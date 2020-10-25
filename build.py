"""This build tool generates the VirtualBox library.py Main COM API."""

from xml.dom import minidom
import os
import re
import hashlib

try:
    import __builtin__ as builtin
except ImportError:
    import builtins as builtin


def pythonic_name(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    if hasattr(builtin, name) is True or name in ["global", "file", "apply"]:
        name += "_p"
    return name


def to_string(value):
    if isinstance(value, str):
        return value
    return value.decode("utf-8")


LIB_IMPORTS = """\
# Complete implementation of VirtualBox's COM API with a Pythonic interface.
#
# Note: Commenting, and API structure generation was carved from 
#       VirtualBox project's VirtualBox.xidl Main API definition.
#
from __future__ import absolute_import
from .library_base import Enum 
from .library_base import Interface 
from .library_base import VBoxError

# Py2 and Py3 compatibility  
try:
    import __builtin__ as builtin 
except:
    import builtins as builtin
try:
    basestring = basestring
except:
    basestring = (str, bytes) 
try:
    baseinteger = (int, long)
except:
    baseinteger = (int, )

"""

LIB_META = """\
vbox_version = '%(vbox_version)s'
lib_version  = %(version)s
lib_app_uuid = '%(app_uuid)s'
lib_uuid     = '%(uuid)s'
xidl_hash    = '%(xidl_hash)s'
"""

LIB_DEFINES = r"""

"""

###########################################################
#
# Doc strip and formatting code
#
###########################################################

remove = ["desc", "tt", "ul", "li", "note", "ol", "h3", "tr", "td", "table", "see"]

replace_words = [
    ("&gt;", ">"),
    ("&lt;", "<"),
    ("&quot;", '"'),
    ("&amp;", "&"),
    ("<desc>", ""),
    ("</desc>", ""),
    ("<desc/>", ""),
    ("<pre>", ""),
    ("</pre>", ""),
    ("<ms>", ""),
    ('<note internal="yes">', ""),
    ("%VirtualBox.VirtualBox", ":py:class:`IVirtualBox`"),
    ("VirtualBox.VirtualBox", ":py:class:`IVirtualBox`"),
    ("%VirtualBox.Session", ":py:class:`ISession`"),
    ("VirtualBox.Session", ":py:class:`ISession`"),
]


def link_class_func(m):
    d = m.groupdict()
    d["func"] = pythonic_name(d["func"])
    d["text"] = d.get("text", "").strip()
    return ":py:func:`%(class)s.%(func)s` %(text)s" % d


def link_class_attr(m):
    d = m.groupdict()
    d["attr"] = pythonic_name(d["attr"])
    d["text"] = d.get("text", "").strip()
    return ":py:attr:`%(class)s.%(attr)s` %(text)s" % d


def link_class(m):
    d = m.groupdict()
    d["text"] = d.get("text", "").strip()
    return ":py:class:`%(class)s` %(text)s" % d


def link_func(m):
    d = m.groupdict()
    d["func"] = pythonic_name(d["func"])
    d["text"] = d.get("text", "").strip()
    return ":py:func:`%(func)s` %(text)s" % d


def bold_text(m):
    return "**%(text)s**" % m.groupdict()


def italic_text(m):
    return "*%(text)s*" % m.groupdict()


def pre_multiline_text(m):
    text = []
    lines = m.groupdict()["text"].splitlines()
    indent = len(lines[0]) - len(lines[0].lstrip())
    for line in lines:
        text.append("     " + line)
    return "\n" + " " * indent + "::\n\n%s\n\n" % "\n".join(text).rstrip()


def desc_text(m):
    return "%(text)s" % m.groupdict()


TEXT = "(?P<text>[^<]+)"
replace_rules = [
    (
        re.compile('<link to="(?P<class>[a-zA-Z]+)::(?P<func>[a-zA-Z]+)"/>'),
        link_class_func,
    ),
    (
        re.compile(
            '<link to="(?P<class>[a-zA-Z]+)::(?P<func>[a-zA-Z]+)">' + TEXT + "</link>"
        ),
        link_class_func,
    ),
    (
        re.compile('<link to="(?P<class>[a-zA-Z]+)_(?P<attr>[a-zA-Z_]+)"/>'),
        link_class_attr,
    ),
    (
        re.compile(
            '<link to="(?P<class>[a-zA-Z]+)_(?P<attr>[a-zA-Z_]+)">' + TEXT + "</link>"
        ),
        link_class_attr,
    ),
    (re.compile('<link to="(?P<class>[a-zA-Z]+)"/>'), link_class),
    (re.compile('<link to="(?P<class>[a-zA-Z]+)">' + TEXT + "</link>"), link_class),
    (re.compile('<link to="#(?P<func>[a-zA-Z]+)"/>'), link_func),
    (re.compile('<link to="#(?P<func>[a-zA-Z]+)">' + TEXT + "</link>"), link_func),
    (re.compile("<b>" + TEXT + "</b>"), bold_text),
    (re.compile("<i>" + TEXT + "</i>"), italic_text),
    (re.compile("<pre>\n(?P<text>[^<]+)</pre>"), pre_multiline_text),
]


def get_doc(node, whitespace=12):
    docnode = node.getElementsByTagName("desc")
    if docnode:
        html = docnode[0].toxml()

        # Strip out stuff we don't want.
        for r in remove:
            html = html.replace("<%s>" % r, "").replace("</%s>" % r, "")
        html, _ = re.subn("(<result).*(</result>)", "", html, flags=re.DOTALL)
        doc = [l.strip() for l in html.splitlines()]
        doc = ("\n" + " " * whitespace).join(doc).rstrip().strip()
        doc = "".join(doc)

        # Run replace rules
        for rule, sub_func in replace_rules:
            m = rule.search(doc)
            while m:
                sub_text = sub_func(m)
                doc = doc.replace(doc[m.start() : m.end()], sub_text)
                m = rule.search(doc)

        # Replace words.
        for pattern, word in replace_words:
            doc = doc.replace(pattern, word)
        return doc
    else:
        return ""


###########################################################
#
#   Generate error code
#
###########################################################
RESULT = '''\
class %(pname)s(VBoxError):
    """%(doc)s"""
    name = '%(name)s'
    value = %(value)s

'''
# Only bother defining the errors explicitly defined
# in VirtualBox.xidl
OLE_ERRORS = [
    ("E_FAIL", "0x80004005", "Unspecified error"),
    ("E_NOINTERFACE", "0x80004002", "No such interface supported"),
    ("E_ACCESSDENIED", "0x80070005", "General access denied error"),
    ("E_NOTIMPL", "0x80004001", "Not implemented"),
    ("E_UNEXPECTED", "0x8000FFFF", "Catastrophic failure"),
    ("E_INVALIDARG", "0x80070057", "One or more arguments are invalid"),
]


def error_name_to_pname(name):
    if name.count("_") > 1:
        pname = "".join([e.title() for e in name.lower().split("_")[2:]])
        pname = "VBoxError%s" % pname
    else:
        pname = name.lower().split("_")[1].title()
        pname = "OleError%s" % pname
    return pname


def build_error_result(name, value, doc):
    pname = error_name_to_pname(name)
    return RESULT % dict(name=name, value=value, doc=doc, pname=pname)


def process_result_node(node):
    name = node.getAttribute("name")
    value = node.getAttribute("value")
    descnode = node.getElementsByTagName("desc")[0]
    doc = descnode.childNodes[0].wholeText.strip()
    return build_error_result(name, value, doc)


###########################################################
#
# Generate Enumeration code
#
###########################################################
ENUM_DEFINE = '''\
class %(name)s(Enum):
    """%(doc)s
    """
    __uuid__ = %(uuid)s
    _enums = %(enums)s '''
ENUM_VALUE = """\
    %(name)s.%(label)s = Enum(%(doc)svalue=%(value)s)"""

ENUM_ROW = """\
        ('%(label)s', %(value)s, 
         '''%(doc)s'''),"""


def process_enum_node(node):
    name = node.getAttribute("name")
    uuid = "'%s'" % node.getAttribute("uuid")
    code = []
    enum_doc = [get_doc(node, 4), "\n"]
    enums = ["["]
    for child in node.childNodes:
        tagname = getattr(child, "tagName", None)
        if tagname != "const":
            continue
        doc = get_doc(child)
        label = str(child.getAttribute("name"))
        value = child.getAttribute("value")
        if "0x" in value:
            value = int(value[2:], 16)
        else:
            value = int(value)
        enums.append(ENUM_ROW % dict(label=label, value=value, doc=doc))

        enum_doc.append(
            """    .. describe:: %s(%s)\n\n            %s\n"""
            % (pythonic_name(label), value, doc)
        )

    enum_doc = "\n".join(enum_doc)
    enums.append("        ]")
    enums = "\n".join(enums)

    # lookup = pprint.pformat(enums, width=4, indent=8)
    code.append(ENUM_DEFINE % dict(name=name, doc=enum_doc, uuid=uuid, enums=enums))
    code.append("\n")
    return "\n".join(code)


###########################################################
#
# Generate Interface code
#
###########################################################
CLASS_DEF = '''\
class %(name)s(%(extends)s):
    """%(doc)s"""
    __uuid__ = '%(uuid)s'
    __wsmap__ = '%(wsmap)s'
    %(event_id)s'''


def process_interface_node(node):
    name = node.getAttribute("name")
    uuid = node.getAttribute("uuid")
    extends = node.getAttribute("extends")
    if extends == "$unknown":
        extends = "Interface"
    elif extends == "$errorinfo":
        extends = "Interface"
    wsmap = node.getAttribute("wsmap")
    doc = get_doc(node, 4)
    if doc:
        doc = "\n    %s\n    " % doc
    event_id = node.getAttribute("id")
    if event_id:
        event_id = pythonic_name(event_id)
        event_id = "id = VBoxEventType.%(event_id)s" % dict(event_id=event_id)
    class_def = CLASS_DEF % dict(
        name=name, extends=extends, doc=doc, uuid=uuid, wsmap=wsmap, event_id=event_id
    )

    code = []
    code.append(class_def)

    for n in node.childNodes:
        name = getattr(n, "tagName", None)
        if name in [None, "desc", "note"]:
            continue
        if name == "attribute":
            code.extend(process_interface_attribute(n))
        elif name == "method":
            code.extend(process_interface_method(n))
        else:
            raise Exception("Unknown interface a member '%s' \n%s" % (name, class_def))
    code.append("")
    return "\n".join(code)


ATTR_GET = '''\
    @property
    def %(pname)s(self):
        """%(doc_action)s %(ntype)s value for '%(name)s'%(doc)s"""
        ret = self._get_attr("%(name)s")
        return %(retval)s'''

ATTR_SET = """
    @%(pname)s.setter
    def %(pname)s(self, value):
%(assert_type)s
        return self._set_attr("%(name)s", value)"""

ATTR_SET_ASSERT_INST = """\
        if not isinstance(value, %(ntype)s):
            raise TypeError("value is not an instance of %(ntype)s")"""

known_types = {
    "wstring": "str",
    "boolean": "bool",
    "long long": "int",
    "long": "int",
    "short": "int",
    "uuid": "str",
    "octet": "str",
    "unsigned long": "int",
    "unsigned short": "int",
    "$unknown": "Interface",
}

python_types = ["str", "bool", "int"]


def type_to_name(t):
    if t in known_types:
        return known_types[t]
    return t


def type_to_name_doc(t):
    if t in known_types:
        return known_types[t]
    return ":class:`%s`" % t


def process_interface_attribute(node):
    name = node.getAttribute("name")
    atype = node.getAttribute("type")
    array = node.getAttribute("safearray") == "yes"
    ntype = type_to_name(atype)
    readonly = node.getAttribute("readonly") == "yes"
    if readonly:
        doc_action = "Get"
    else:
        if array:
            print("TODO: %s %s get or set with array" % (name, atype))
        doc_action = "Get or set"
    rdoc = get_doc(node, 8)
    if rdoc:
        doc = "\n        %s\n        " % (rdoc)
    else:
        doc = ""

    code = []
    pname = pythonic_name(name)
    if array:
        if ntype not in python_types:
            retval = "[%s(a) for a in ret]" % ntype
        else:
            retval = "ret"
    else:
        if ntype not in python_types:
            retval = "%s(ret)" % (ntype)
        else:
            retval = "ret"
    code.append(
        ATTR_GET
        % dict(
            name=name,
            pname=pname,
            ntype=ntype,
            doc=doc,
            doc_action=doc_action,
            retval=retval,
        )
    )

    # build setter
    if not readonly:
        if rdoc:
            doc = "\n        %s\n        " % (rdoc)

        if ntype == "str":
            assert_type = ATTR_SET_ASSERT_INST % (dict(ntype="basestring"))
        elif ntype == "int":
            assert_type = ATTR_SET_ASSERT_INST % (dict(ntype="baseinteger"))
        else:
            assert_type = ATTR_SET_ASSERT_INST % (dict(ntype=ntype))
        code.append(ATTR_SET % dict(name=name, pname=pname, assert_type=assert_type))
    code.append("")
    return code


METHOD_FUNC = '''\
    def %(pname)s(self%(inparams)s):
        """%(doc)s
        """'''

METHOD_DOC_PARAM = """\
        %(io)s %(pname)s of type %(ptype)s%(doc)s
"""

METHOD_DOC_RAISES = """\
        raises %(name)s%(doc)s
        """

METHOD_ASSERT_IN_INST = """\
        if not isinstance(%(invar)s, %(invartype)s):
            raise TypeError("%(invar)s can only be an instance of type %(invartype)s")"""

METHOD_ASSERT_ARRAY_IN = """\
        for a in %(invar)s[:10]:
            if not isinstance(a, %(invartype)s):
                raise TypeError("array can only contain objects of type %(invartype)s")"""

METHOD_ASSERT_ARRAY_IN_INST = """\
        for a in %(invar)s[:10]:
            if not isinstance(a, %(invartype)s):
                raise TypeError(
                        "array can only contain objects of type %(invartype)s")"""

METHOD_CALL = """\
        %(outvars)sself._call("%(name)s"%(in_p)s)"""

METHOD_OUT_CONV = """\
        %(name)s = %(convfunc)s"""

METHOD_RETURN = """\
        %(retcmd)s"""


def process_interface_method(node):
    def process_result(c):
        name = c.getAttribute("name")
        cname = ":class:`%s`" % error_name_to_pname(name)
        d = c.childNodes[0]
        cdoc = getattr(d, "wholeText", "").strip()
        if cdoc:
            cdoc = "\n            %s" % cdoc
        return (cname, cdoc)

    method_name = node.getAttribute("name")
    method_doc = get_doc(node, 8)

    ret_param = None
    params = []
    raises = []
    for c in node.childNodes:
        name = getattr(c, "tagName", None)
        if name in [None, "note"]:
            continue
        if name == "desc":
            for e in c.childNodes:
                n = getattr(e, "tagName", None)
                if n == "result":
                    raises.append(process_result(e))
        elif name == "result":
            raises.append(process_result(c))
        elif name == "param":
            cname = c.getAttribute("name")
            cdoc = get_doc(c)
            atype = c.getAttribute("type")
            cio = c.getAttribute("dir")
            array = c.getAttribute("safearray")
            if cio in ["in", "out"]:
                params.append((cname, cio, cdoc, atype, array))
            elif cio == "return":
                params.append((cname, cio, cdoc, atype, array))
                ret_param = (cname, cdoc, atype, array)
            else:
                raise Exception("Unknown param type '%s' for %s" % (cio, method_name))
        else:
            raise Exception("Unknown method component '%s'" % name)

    # function doc
    doc = [method_doc]
    doc.append("")
    for n, io, d, t, _ in params:
        ptype = type_to_name_doc(t)
        if d:
            d = "\n            %s" % d
        doc.append(
            METHOD_DOC_PARAM % dict(io=io, pname=pythonic_name(n), doc=d, ptype=ptype)
        )
    for n, d in raises:
        doc.append(METHOD_DOC_RAISES % dict(doc=d, name=n))
    doc = "\n".join(doc)

    # function definition
    inparams = [pythonic_name(n) for n, io, _, _, _ in params if io == "in"]
    inparams_raw = ", ".join(inparams)
    if inparams_raw:
        inparams = ", %s" % inparams_raw
    else:
        inparams = ""

    func = []
    func.append(
        METHOD_FUNC % dict(pname=pythonic_name(method_name), doc=doc, inparams=inparams)
    )

    # prep METOD_CALL vars and insert ASSERT IN
    outvars = []
    out_p = []
    for n, io, d, t, array in params:
        name = pythonic_name(n)
        atype = type_to_name(t)
        if io == "in":
            if array:
                invartype = "list"
            else:
                invartype = atype

            if invartype == "str":
                func.append(
                    METHOD_ASSERT_IN_INST % dict(invar=name, invartype="basestring")
                )
            elif invartype == "int":
                func.append(
                    METHOD_ASSERT_IN_INST % dict(invar=name, invartype="baseinteger")
                )
            else:
                func.append(
                    METHOD_ASSERT_IN_INST % dict(invar=name, invartype=invartype)
                )
            if array:
                if atype == "str":
                    func.append(
                        METHOD_ASSERT_ARRAY_IN_INST
                        % dict(invar=name, invartype="basestring")
                    )
                elif atype == "int":
                    func.append(
                        METHOD_ASSERT_ARRAY_IN_INST
                        % dict(invar=name, invartype="baseinteger")
                    )
                else:
                    func.append(
                        METHOD_ASSERT_ARRAY_IN_INST % dict(invar=name, invartype=atype)
                    )
        elif io == "out":
            outvars.append(name)
            out_p.append((name, atype, array))

    if ret_param is not None:
        n, _, t, a = ret_param
        name = pythonic_name(n)
        atype = type_to_name(t)
        # xpcom returns retval before out vars
        outvars.insert(0, name)
        out_p.insert(0, (name, atype, array))

    if inparams_raw:
        in_p = ",\n%sin_p=[%s]" % (" " * 21, inparams_raw)
    else:
        in_p = ""

    if outvars:
        if len(outvars) > 1:
            retvars = "(%s)" % (", ".join(outvars))
        else:
            retvars = outvars[0]
        outvars = "%s = " % (retvars)
    else:
        outvars = ""
        retvars = ""

    func.append(METHOD_CALL % dict(outvars=outvars, name=method_name, in_p=in_p))

    for name, atype, array in out_p:
        if atype in python_types:
            continue

        if array:
            convfunc = "[%s(a) for a in %s]" % (atype, name)
        else:
            convfunc = "%s(%s)" % (atype, name)
        func.append(METHOD_OUT_CONV % dict(name=name, convfunc=convfunc))

    if retvars:
        retcmd = "return %s" % retvars
        func.append(METHOD_RETURN % dict(retcmd=retcmd))
    func.append("")
    return func


def preprocess(xidl, target):
    lines = []
    emit = True
    for line in xidl.splitlines():
        line = line.strip()
        if line.startswith(b"<if target="):
            if target in line:
                emit = True
            else:
                emit = False
            continue
        elif line == b"</if>":
            emit = True
            continue
        if emit:
            lines.append(line)
    return b"\n".join(lines)


###########################################################
#
#  Where it all begins...
#
###########################################################


def get_vbox_version(config_kmk):
    "Return the vbox config major, minor, build"
    with open(config_kmk, "rb") as f:
        config = f.read()
    major = b"6"  # re.search(b"VBOX_VERSION_MAJOR = (?P<major>[\d])", config).groupdict()['major']
    minor = b"1"  # re.search(b"VBOX_VERSION_MINOR = (?P<minor>[\d])", config).groupdict()['minor']
    build = b"16"  # re.search(b"VBOX_VERSION_BUILD = (?P<build>[\d])", config).groupdict()['build']
    return b".".join([major, minor, build])


def main():
    virtualbox_xidl = "VirtualBox.xidl"
    config_kmk = "Config.kmk"

    print("Create new virtualbox/library.py")
    xidl = open(virtualbox_xidl, "rb").read()
    xidl = preprocess(xidl, target=b"xpidl")

    xml = minidom.parseString(xidl)

    # Get the idl description
    idl = xml.getElementsByTagName("idl")
    assert len(idl) == 1
    idl = idl[0]
    lib_doc = '''__doc__ = """\\\n  %s\n"""\n\n''' % get_doc(idl, 0)

    # Process the library

    library = xml.getElementsByTagName("library")
    assert len(library) == 1
    library = library[0]

    # 5.2 introduced <library><application> ... </application></library>
    applications = xml.getElementsByTagName("application")
    if applications:
        for application in applications:
            name = application.attributes.get("name", None)
            if name is not None:
                if "VirtualBox" == name.value:
                    break
        else:
            raise ValueError("Failed to find VirtualBox application")
        app_uuid = application.getAttribute("uuid")
        virtualbox_application = application
    else:
        app_uuid = library.getAttribute("appUuid")
        virtualbox_application = library

    # Iterate each element under the virtualbox application node
    source = dict(result=[], enum=[], interface=[])
    for node in virtualbox_application.childNodes:
        name = getattr(node, "tagName", None)
        if name is None:
            continue
        if name == "result":
            source["result"].append(process_result_node(node))
        elif name == "enum":
            source["enum"].append(process_enum_node(node))
        elif name == "interface":
            source["interface"].append(process_interface_node(node))

    # Add OLE errors to 'result'
    for args in OLE_ERRORS:
        source["result"].append(build_error_result(*args))

    # get lib meta
    vbox_version = get_vbox_version(config_kmk)
    uuid = library.getAttribute("uuid")
    version = library.getAttribute("version")
    xidl_hash = hashlib.md5(xidl).hexdigest()
    lib_meta = LIB_META % dict(
        vbox_version=to_string(vbox_version),
        uuid=to_string(uuid),
        version=to_string(version),
        app_uuid=to_string(app_uuid),
        xidl_hash=to_string(xidl_hash),
    )

    code = []
    code.append(LIB_IMPORTS)
    code.append(lib_doc)
    code.append(lib_meta)
    code.append(LIB_DEFINES)
    code.extend(source["result"])
    code.extend(source["enum"])
    code.extend(source["interface"])
    code = b"\n".join(
        [c.encode("utf-8") if not isinstance(c, bytes) else c for c in code]
    )
    print("   vbox version : %s" % to_string(vbox_version))
    print("   xidl hash    : %s" % xidl_hash)
    print("   version      : %s" % version)
    print("   line count   : %s" % code.count(b"\n"))
    library_path = os.path.join(".", "virtualbox", "library.py")
    if os.path.exists(library_path):
        os.unlink(library_path)
    with open(library_path, "wb") as f:
        f.write(code)


if __name__ == "__main__":
    main()
