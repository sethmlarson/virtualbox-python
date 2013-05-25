from xml.dom import minidom
import pprint
import sys
import os
import re
import hashlib

try:
    import __builtin__ as builtin 
except:
    import builtin


def pythonic_name(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    if hasattr(builtin, name) is True or name in ['global']:
        name += "_p"
    return name


LIB_IMPORTS = """\
# A Pythonic VirtalBox Main API
#
# By Michael Dorman.
# Email mjdorma+pyvbox@gmail.com
#
# Note: Commenting, and API structure generation was carved from 
#       VirtualBox project's VirtualBox.xidl Main API definition.
#
import re
try:
    import __builtin__ as builtin 
except:
    import builtin

"""

LIB_META = """\
lib_version = %(version)s
lib_app_uuid = '%(app_uuid)s'
lib_uuid = '%(uuid)s'
xidl_hash = '%(xidl_hash)s'
"""

LIB_DEFINES = r'''
def pythonic_name(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    if hasattr(builtin, name) is True or name in ['global']:
        name += "_p"
    return name


class EnumType(type):
    def __init__(cls, name, bases, dct):
        cls.value = None
        cls.lookup_label = {v:k for k, v in cls.lookup_value.items()}
        for name, v in cls.lookup_value.items():
            setattr(cls, pythonic_name(name), cls(v))

    def __getitem__(cls, k):
        if not hasattr(cls, k):
            raise KeyError("%s has no key %s" % cls.__name__, k)
        return getattr(cls, k)

    def __getattribute__(cls, k):
        return type.__getattribute__(cls, k)


class Enum(object):
    lookup_value = {}
    __metaclass__ = EnumType
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return self.lookup_label[self.value]

    def __int__(self):
        return self.value

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.value)

    def __eq__(self, k):
        if isinstance(k, self.__class__):
            return k.value == self.value
        return False

    def __getitem__(self, k):
        return self.__class__[k]


class Interface(object):

    def __init__(self, interface=None):
        if interface is None:
            self._i = interface
        else:
            self._i = interface

    def _change_to_realtype(self, value):
        if isinstance(value, Interface):
            return value._i
        elif isinstance(value, Enum):
            return int(value)
        else:
            return value

    def _set_attr(self, name, value):
        setattr(self._i, name, self._change_to_realtype(value))

    def _get_attr(self, name):
        return getattr(self._i, name)

    def _call_method(self, name, in_p=[]):
        global vbox_error
        m = getattr(self._i, name)
        in_params = [self._change_to_realtype(p) for p in in_p]
        try:
            ret = m(*in_params)
        except Exception as exc:
            if hasattr(exc, 'errno'):
                errno = exc.errno & 0xFFFFFFFF
                errclass = vbox_error.get(errno, VBoxError)
                errobj = errclass()
                errobj.value = errno
            else:
                errobj = VBoxError()
            errobj.msg = getattr(exc, 'msg', exc.message)
            raise errobj
        return ret


class VBoxError(Exception): 
    """Generic VBoxError"""
    name = "undef"
    value = -1
    msg = ""
    def __str__(self):
        return "0x%x (%s)" % (self.value, self.msg)


#container lookup for the different error types
vbox_error = {}

'''

remove = ['desc', 'pre', 'tt', 'ul', 'li', 'note', 'b', 'ol', 'i', 'h3',
           'tr', 'td', 'table', 'see']

def get_doc(node):
    docnode = node.getElementsByTagName('desc')
    if docnode:
        xml = docnode[0].toxml()
        html = xml.replace('&gt;', '>').replace('&lt;', '<')
        html = html.replace('&quot;', '"')
        for r in remove:
            html = html.replace('<%s>' % r, '').replace('</%s>' % r, '')
        html, _ = re.subn('(<result).*(</result>)', '', html, flags=re.DOTALL)
        return html.strip()
    else:
        return ''


###########################################################
#
#
#
RESULT = '''\
class %(pname)s(VBoxError):
    """%(doc)s"""
    name = '%(name)s'
    value = %(value)s
vbox_error[%(value)s] = %(pname)s

'''


def process_result(node):
    name = node.getAttribute('name')
    pname = "".join([e.title() for e in name.lower().split('_')[2:]])
    pname = "VBoxError%s" % pname
    value = node.getAttribute('value')
    descnode = node.getElementsByTagName('desc')[0]
    doc = descnode.childNodes[0].wholeText.strip()
    return RESULT % dict(name=name, value=value, doc=doc, pname=pname)


###########################################################
#
#
#
ENUM_DEFINE = '''\
class %(name)s(Enum):
    """(%(doc)s)"""
    uuid = %(uuid)s
    lookup_value = %(lookup_value)s '''
ENUM_VALUE = """\
    %(name)s.%(label)s = Enum(%(doc)svalue=%(value)s)"""


def process_enum(node):
    name = node.getAttribute('name')
    uuid = "'%s'" % node.getAttribute('uuid')
    code = []
    enum_doc = get_doc(node)
    lookup = {}
    lookup_value = {}
    lookup_label = {}
    for child in node.childNodes:
        tagname = getattr(child, 'tagName', None)
        if tagname != 'const':
            continue
        doc = get_doc(child)
        label = str(child.getAttribute('name'))
        value = child.getAttribute('value')
        if '0x' in value:
            value = int(value[2:], 16)
        else:
            value = int(value)
        lookup_value[label] = value
        lookup_label[value] = label
        lookup[label] = (value, doc)
        #code.append(ENUM_VALUE % dict(name=name, label=label,
        #                              value=value, doc=doc))
    lookup_label = pprint.pformat(lookup_label, width=4, indent=8)
    lookup_value = pprint.pformat(lookup_value, width=4, indent=8)
    code.append(ENUM_DEFINE % dict(name=name, doc=enum_doc, 
                                   uuid=uuid, lookup_value=lookup_value))

    python_name = pythonic_name(name)
    code.append('\n')
    return "\n".join(code)


###########################################################
#
#
#
CLASS_DEF = '''\
class %(name)s(%(extends)s):
    """%(doc)s"""
    uuid = '%(uuid)s'
    wsmap = '%(wsmap)s'
    %(event_id)s'''

CLASSES = {'IVirtualBox':"@virtualbox.org/VirtualBox;1",
           'ISession':"@virtualbox.org/Session;1"}

INIT_METHOD = """\
    def __init__(self):
        import xpcom.components
        classobj = xpcom.components.classes["%(class_ref)s"]
        self._i = classobj.createInstance()

"""

def process_interface(node):
    name = node.getAttribute('name')
    uuid = node.getAttribute('uuid')
    extends = node.getAttribute('extends')
    if extends == '$unknown':
        extends = 'Interface'
    elif extends == '$errorinfo':
        extends = 'Interface'
    wsmap = node.getAttribute('wsmap')
    doc = get_doc(node)
    if doc:
        doc = "\n    %s\n    "%doc
    event_id = node.getAttribute('id')
    if event_id:
        event_id = pythonic_name(event_id)
        event_id = "id = VBoxEventType.%(event_id)s" % dict(event_id=event_id)
    class_def = CLASS_DEF % dict(name=name, 
        extends=extends, doc=doc, uuid=uuid, wsmap=wsmap,
        event_id=event_id)

    code = []
    code.append(class_def)

    for n in node.childNodes:
        name = getattr(n, 'tagName', None)
        if name in [None, 'desc', 'note']:
            continue
        if name == 'attribute':
            code.extend(process_interface_attribute(n))
        elif name == 'method':
            code.extend(process_interface_method(n))
        else:
            raise Exception("Unknown interface a member %s" % name)
    code.append('')
    return "\n".join(code) 


ATTR_GET = '''\
    @property
    def %(pname)s(self):
        """%(doc_action)s %(ntype)s value for '%(name)s'%(doc)s"""
        ret = self.%(callname)s
        return %(retval)s 
'''
ATTR_SET = '''\
    @%(pname)s.setter
    def %(pname)s(self, value):
        assert isinstance(value, %(ntype)s), \\
                "value is not an instance of %(ntype)s"
        return self._set_attr('%(name)s', value)
'''

known_types = {'wstring':'str',
               'boolean':'bool', 
               'long long':'int',
               'long':'int',
               'short':'int',
               'uuid':'str',
               'octet':'str',
               'unsigned long':'int',
               'unsigned short':'int',
               '$unknown':'Interface'}


def type_to_name(t):
    if t in known_types:
        return known_types[t]
    return t 


def process_interface_attribute(node):
    name = node.getAttribute('name')
    atype = node.getAttribute('type')
    array = node.getAttribute('safearray') == 'yes'
    ntype = type_to_name(atype)
    readonly = node.getAttribute('readonly') == 'yes'
    if readonly:
        doc_action = "Get"
    else:
        doc_action = "Get or set"
    rdoc = get_doc(node)
    if rdoc:
        doc = "\n        %s\n        " % (rdoc)
    else:
        doc = ''

    code = []
    pname = pythonic_name(name)
    if array:
        callname = "_call_method('get%s')" % (name[0].upper() + name[1:])
        retval = "[%s(a) for a in ret]" % ntype
    else:
        callname = "_get_attr('%s')" % name
        retval = "%s(ret)" % (ntype)
    code.append(ATTR_GET % dict(name=name, pname=pname, callname=callname, ntype=ntype, 
                doc=doc, doc_action=doc_action,
                retval=retval))
    if not readonly:
        if rdoc: 
            doc = "\n        %s\n        " % (rdoc)
        code.append(ATTR_SET % dict(name=name, pname=pname,
                        ntype=ntype))
    return code


METHOD_FUNC = '''\
    def %(pname)s(self%(inparams)s):
        """%(doc)s
        """'''

METHOD_DOC_PARAM = '''\
        %(io)s %(pname)s of type %(ptype)s%(doc)s
'''

METHOD_DOC_RAISES = '''\
        raises %(name)s%(doc)s
        '''

METHOD_ASSERT_IN = '''\
        assert isinstance(%(invar)s, %(invartype)s), \\
                "%(invar)s is not an instance of %(invartype)s"'''

METHOD_CALL = '''\
        %(outvars)sself._call_method('%(name)s'%(in_p)s)'''

METHOD_OUT_CONV = '''\
        %(name)s = %(atype)s(%(name)s)'''

METHOD_RETURN = '''\
        %(retcmd)s'''

def process_interface_method(node):
    def process_result(c):
        cname = c.getAttribute('name')
        d = c.childNodes[0]
        cdoc = getattr(d, 'wholeText', '').strip()
        if cdoc:
            cdoc = "\n            %s" % cdoc
        return (cname, cdoc)

    method_name = node.getAttribute('name')
    method_doc = get_doc(node)

    ret_param = None
    params = []
    raises = []
    for c in node.childNodes:        
        name = getattr(c, 'tagName', None)
        if name in [None, 'note']:
            continue
        if name == 'desc':
            for e in c.childNodes:
                n = getattr(e, 'tagName', None)
                if n == 'result':
                    raises.append(process_result(e))                
        elif name == 'result':
            raises.append(process_result(c))
        elif name == 'param':
            cname = c.getAttribute('name')
            cdoc = get_doc(c)
            atype = c.getAttribute('type')
            cio = c.getAttribute('dir')
            if cio in ['in', 'out']:
                params.append((cname, cio, cdoc, atype))
            elif cio == 'return':
                params.append((cname, cio, cdoc, atype))
                ret_param = (cname, cdoc, atype)
            else:
                raise Exception("Unknown param type '%s' for %s" % \
                        (cio, method_name))
        else:
            raise Exception("Unknown method component '%s'" % name)

    #function doc
    doc = [method_doc]
    doc.append('')
    for n, io, d, t in params: 
        ptype = type_to_name(t)
        if d:
            d = "\n            %s" % d
        doc.append(METHOD_DOC_PARAM % dict(io=io, pname=pythonic_name(n), 
                                doc=d, ptype=ptype))
    for n, d in raises:
        doc.append(METHOD_DOC_RAISES % dict(doc=d, name=n))
    doc = "\n".join(doc)

    #function definition 
    inparams = [pythonic_name(n) for n, io, _, _ in params if io == 'in']
    inparams_raw = ", ".join(inparams)
    if inparams_raw:
        inparams = ", %s" % inparams_raw 
    else:
        inparams = ''

    func = []
    func.append(METHOD_FUNC % dict(pname=pythonic_name(method_name),
                                doc=doc,
                                inparams=inparams))

    # prep METOD_CALL vars and insert ASSERT IN 
    outvars = []
    out_p = []
    for n, io, d, t in params:
        name = pythonic_name(n)
        atype = type_to_name(t)
        if io == 'in':
            func.append(METHOD_ASSERT_IN % dict(invar=name,
                                                invartype=atype))
        elif io == 'out':
            outvars.append(name)
            out_p.append((name, atype))
    
    if ret_param is not None:
        n, _, t = ret_param
        name = pythonic_name(n)
        atype = type_to_name(t)
        outvars.append(name)
        out_p.append((name, atype))

    if inparams_raw:
        in_p = ",\n%sin_p=[%s]" % (" " * 21, inparams_raw)
    else:
        in_p = ''

    if outvars:
        if len(outvars) > 1:
            retvars = "(%s)" % (", ".join(outvars))
        else:
            retvars = outvars[0]
        outvars = "%s = " % (retvars)
    else:
        outvars = ''

    func.append(METHOD_CALL % dict(outvars=outvars, name=method_name,
        in_p=in_p))

    # build retcmd
    if out_p:
        retcmd = ["%s(%s)" % (atype, name) for name, atype in out_p]
        retcmd = ", ".join(retcmd)
        if len(out_p) > 1:
            retcmd = "(%s)" % retcmd 
        retcmd = "return %s\n" % retcmd
    else:
        retcmd = ''
    
    func.append(METHOD_RETURN % dict(retcmd=retcmd))
        
    return func


###########################################################
#
#
#
XIDL = """\
http://www.virtualbox.org/svn/vbox/trunk/src/VBox/Main/idl/VirtualBox.xidl"""

def main(virtualbox_xidl):
    if not os.path.exists(virtualbox_xidl):
        os.system('wget %s' % XIDL)
        virtualbox_xidl = 'VirtualBox.xidl'
        assert os.path.exists(virtualbox_xidl), "failed to download %s" % XIDL
            

    print("Create new virtualbox/library.py")
    xidl = open(virtualbox_xidl, 'rb').read()
        
    xml = minidom.parseString(xidl)
    
    # Get the idl description
    idl = xml.getElementsByTagName('idl')
    assert len(idl) == 1
    idl = idl[0]
    lib_doc = '''__doc__ = """\\\n  %s\n"""\n\n''' %get_doc(idl)

    # Process the library
    library = xml.getElementsByTagName('library')
    assert len(library) == 1
    library = library[0]

    source = dict(result=[], enum=[], interface=[])
    for node in library.childNodes:
        name = getattr(node, 'tagName', None)
        if name is None:
            continue
        if name == 'result':
            source['result'].append(process_result(node))
        elif name == 'enum':
            source['enum'].append(process_enum(node))
        elif name == 'interface':
            source['interface'].append(process_interface(node))

    #get lib meta
    uuid = library.getAttribute('uuid')
    version = library.getAttribute('version')
    app_uuid = library.getAttribute('appUuid')
    xidl_hash = hashlib.md5(xidl).hexdigest()
    lib_meta = LIB_META % dict(uuid=uuid, version=version, app_uuid=app_uuid,
                xidl_hash=xidl_hash)

    code = []
    code.append(LIB_IMPORTS)
    code.append(lib_doc)
    code.append(lib_meta)
    code.append(LIB_DEFINES)
    code.extend(source['result'])
    code.extend(source['enum'])
    code.extend(source['interface'])
    code = "\n".join(code)
    print("   xidl hash  : %s" % xidl_hash)
    print("   version    : %s" % version) 
    print("   line count : %s" % code.count("\n"))
    with open('virtualbox/library.py', 'wb') as f:
        f.write(code)


if __name__ == '__main__':
    path = 'VirtualBox.xidl'
    if sys.argv[1:]:
        path = sys.argv[1]
    main(path)

