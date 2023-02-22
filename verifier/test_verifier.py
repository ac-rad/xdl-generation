import verify

def test_01():  # Correct XDL
    f = open("verifier/data/test01.xml", "r")
    xdl = f.read()
    errors = verify.verify_xdl(xdl)
    assert not errors  # check if error list is empty

def test_02():  # Invalid as XML
    f = open("verifier/data/test02.xml", "r")
    xdl = f.read()
    errors = verify.verify_xdl(xdl)
    assert isinstance(errors, str)

def test_03():  # Invalid action
    f = open("verifier/data/test03.xml", "r")
    xdl = f.read()
    errors = verify.verify_xdl(xdl)
    assert isinstance(errors, list)
    assert len(errors) == 1
    assert errors[0]["step"] == '<Mix vessel="beaker" reagent="sugar" amount="10 g" />'

def test_04():  # Invalid property
    f = open("verifier/data/test04.xml", "r")
    xdl = f.read()
    errors = verify.verify_xdl(xdl)
    assert isinstance(errors, list)
    assert len(errors) == 1
    assert errors[0]["step"] == '<Add vesel="beaker" reagent="water" amount="10 mL" />'

def test_05():  # Undefined hardware
    f = open("verifier/data/test05.xml", "r")
    xdl = f.read()
    errors = verify.verify_xdl(xdl)
    assert isinstance(errors, list)
    assert len(errors) == 1
    assert errors[0]["step"] == '<Transfer from_vessel="beaker" to_vessel="beaker2" />'

def test_06():  # Undefined reagent
    f = open("verifier/data/test06.xml", "r")
    xdl = f.read()
    errors = verify.verify_xdl(xdl)
    assert isinstance(errors, list)
    assert len(errors) == 1
    assert errors[0]["step"] == '<Add vessel="beaker" reagent="sugar" amount="10 g" />'

def test_07():  # Multiple errors
    f = open("verifier/data/test07.xml", "r")
    xdl = f.read()
    errors = verify.verify_xdl(xdl)
    assert isinstance(errors, list)
    assert len(errors) == 2
    assert errors[0]["step"] == '<Add vesel="beaker" reagent="water" amount="10 mL" />'
    assert errors[1]["step"] == '<Add vessel="beaker" reagent="sugar" amount="10 g" />'

def test_09():  # Reagent property
    f = open("verifier/data/test09.xml", "r")
    xdl = f.read()
    errors = verify.verify_xdl(xdl)
    assert isinstance(errors, list)
    assert len(errors) == 2
    assert errors[0]["step"] == '<Reagent name="vinegar" solid="true" />'
    assert errors[1]["step"] == '<Reagent inchi="InChI=1S/ClH.Na/h1H;/q;+1/p-1" />'

def test_08():  # using hardware that not in available_hardware list
    f = open("verifier/data/test08.xml", "r")
    xdl = f.read()
    errors = verify.verify_xdl(xdl, available_hardware=['beaker'])
    print(errors)
    assert isinstance(errors, list)
    assert len(errors) == 1
    assert errors[0]["hardware"] == '<Component id="beaker2" type="beaker" />'

