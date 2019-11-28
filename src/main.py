# coding=utf-8

'''
Generate notepad filled with BDC info
V1.1.0
Author: Remi NGUYEN

'''
from bs4 import BeautifulSoup
import re
import sys
import subprocess
import ctypes
import os
import time

def compareDate(date1):
	# return True if  date1 < date 2 else False
	#strftime("%Y-%m-%d", gmtime())
	date_bdc = find_termination_date(soup).split('-')
	date1 = datetime.datetime(date1[2], date[1], date[0])
	present = datetime.now()
def Mbox(soup, bdc, operator, vlan, type_, serviceId):
	title = "{} {}".format(bdc, operator)
	message = ""
	if type_ == "RESILIATION":
		date = find_termination_date(soup)

	if vlan != "" and type_ == "ACTIVATION":
		message += "Utilisez le vlan {}\n".format(vlan)
	if "ORANGE" in operator and type_ == "ACTIVATION":
		message += "Port usager: speed-duplex 1000-full-duplex\n"
	if "BK" in serviceId:
		message += "Attention au service ID " + serviceId
	if message != "":
		return ctypes.windll.user32.MessageBoxW(0, message, title, 0)

def my_soup(infile):
    # Manage option from argv
    # Retreive HTML code from webtool page
    name_file = str()
    if infile != None:
        name_file = infile
    else:
        name_file = str(input("file.htm>>"))
    # Append .htm extension if not in input
    if "htm" not in name_file:
        name_file += ".htm"
    file_html = open(name_file, 'r', encoding="utf8")
    soup = BeautifulSoup(file_html, 'html.parser')
    file_html.close()

    return soup

"""
Argument: type_obj soup, contains html code
Return request type := ACTIVATION | RESILIATION
"""
def find_type(soup):
    type_ = soup.find_all(id="type_demande")
    type_regex = r'RESILIATION|ACTIVATION|MODIFICATION'
    type_match = re.findall(type_regex, str(type_[0]))

    return type_match[0] if type_match else -1

"""
Argument: type_obj soup, contains html code
Return Service ID
"""
def find_service_id(soup):
    service_id = soup.find_all('div', class_='col-md-9')
    service_regex = r'(FR\d+|AC\d+|BK\d+)'
    service_match = re.findall(service_regex, str(service_id))

    return service_match[0] if service_match else ""

"""
Argument: obj soup, contains html code
Return DSP name
"""
def find_dsp(soup):
    dsp = soup.find_all(id="dsp_nom_commun")
    #dsp_regex = r'value="([ !@#$%^&*()_+=a-zA-Z0-9,./\|<>?:;-]*)"'
    dsp_regex = r'value="([^"]*)"'
    dsp_match = re.findall(dsp_regex, str(dsp))

    return dsp_match[0] if dsp_match else -1

"""
Argument: type_obj soup, contains html code
Return Operator name and its IPAM format(optional)
"""
def find_operator(soup):
    operator = soup.find_all(id="operateur_nom")
    operator_regex = r'value="(\w+[^"]*)"'
    operator_match = re.findall(operator_regex, str(operator))

    # Operator name for IPAM
    op_name = operator_match[0]
    op_ipam = op_name.split(" ")
    op_ipam = "_".join(op_ipam)

    return op_name, op_ipam

"""
Argument: type_obj soup, contains html code
Return Termination Date
"""
def find_termination_date(soup):
    date = soup.find_all(id="date_activation")
    date_regex = r'value="(\d+[-]{1}\d+[-]{1}\d+)"'
    date_match = re.findall(date_regex, str(date))

    return date_match[0] if date_match else []

"""
Fct: Change date format Y/m/d -> d/m/Y
Argument: type_string date Y/m/d
Return termination date
"""
def date_format(date):
    if date:
        date = date.split('-')
        date[0],date[-1] = date[-1],date[0]
        return "-".join(date)
    return ""

"""
Argument: type_obj soup
Return BDC
"""
def find_bdc(soup):
    bdc = soup.find_all(id="ref_bdc")
    bdc_regex = r'value="([A-Z1-9]{3}[0-9-]+)"'
    bdc_match = re.findall(bdc_regex, str(bdc))

    return bdc_match[0]

"""
Argument: type_obj soup
Return debit and debit minimum
"""
def find_debit(soup):
    debit = soup.find_all(id="debit")
    debit_regex = r'value="(\d+\w*)"'
    debit_match = re.findall(debit_regex, str(debit))

    debit_min_s = soup.find_all(id="debit_minimum")
    debit_min = re.findall(debit_regex, str(debit_min_s))
    if debit_min and debit_match:
        return debit_min[0] + "-" + debit_match[0]
    return debit_match[0] if debit_match else ''

"""
Argument: type_obj soup
Return VLAN if indicated
"""
def find_vlan(soup):
    vlan = soup.find_all(id="num_vlan")
    vlan_regex = r'value="(\d+)'
    vlan_match = re.findall(vlan_regex, str(vlan))
    return vlan_match[0] if vlan_match else ""

"""
Argument: type_obj soup
Return site A
"""
def find_site_a(soup):
        site_a = soup.find_all(id="nom_site_a")
        site_regex = r'value="([^"]*)"'
        site_a_match = re.findall(site_regex, str(site_a))
        client = site_a_match[0]
        if '&amp'in site_a_match[0]:
            client = site_a_match[0].replace("&amp;", "&")
        print
        return client if site_a_match else ""

"""
Case: activation and IPAM
Argument: service_id FRXXXXXX | ACXXXXXX
Return PROD_BPE|PROD_BPEA
"""
def find_prod_bp(service_id):
    return "PROD_BPEA" if "AC" in service_id else "PROD_BPE"
"""
Fct: retrieve information on POP slot port, @MAC
Argument: type_obj soup
Return type_string POP information
"""
def find_pop_info(soup):
    pop_info = soup.find_all(id="commentaire", rows="5")
    info_regex = r'rows="5">([\s\S]*)<'
    info_comp = str(re.findall(info_regex, str(pop_info[0]))[0])
    #print("\n" + info_comp)
    return info_comp

def find_fr_collecte(soup):
    fr_info = soup.find_all(id="fr_collecte")
    if not fr_info:
    	return ""
    fr_regex = r'(CN\d+|FR\d+|AC\d+)'
    fr_collecte = re.findall(fr_regex, str(fr_info[0]))
    return fr_collecte[0] if fr_collecte else ""

def process(oper, s_id, type_activ):
	pass

if __name__ == "__main__":
    OPENFILE = False
    HTMLFILE = None
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == '-o':
                OPENFILE = True
            elif  arg[0] == '-':
                print("Error! Option {} not recognized".format(arg))
                sys.exit(1)
            elif HTMLFILE == None:
                HTMLFILE = str(arg)
            else:
                print("Wrong Usage! >>python autotool.py [-o] <file>")
                sys.exit(1)
    soup = my_soup(HTMLFILE)

    type_ = find_type(soup)
    service_id_ = find_service_id(soup)
    dsp_ = "DSP\t\t" + find_dsp(soup)
    operator_name_, op_ipam = find_operator(soup)

    vlan_ = find_vlan(soup)
    vlan_id = vlan_
    name_ = service_id_
    if type_ == "ACTIVATION":
        name_ = "-".join([service_id_, op_ipam]) + "-" + vlan_

    operator_ = "OPERATEUR\t" + operator_name_
    prod_bp_ = "ETAT\t\t" + find_prod_bp(service_id_)
    date_ = ""

    if type_ == "RESILIATION":
        date_ = find_termination_date(soup)
        if date_ != "":
            date_ = "DATE\t" + date_format(date_)
    bdc_ = find_bdc(soup)
    bdc_box = bdc_
    debit_ = "DEBIT\t" + find_debit(soup)
    vlan_ = "VLAN\t" + vlan_
    fr_collecte_ = find_fr_collecte(soup)
    siteA = find_site_a(soup)
    site_a_ = "SITE A: " + siteA + "\n"
    site_b_ = "SITE B: " + fr_collecte_ + "\n"



    info_complementaires = find_pop_info(soup)
    # Write things in file
    file_name_ = bdc_ + ".txt"
    my_file = open(file_name_, 'w', encoding="utf-8")
    #FIXME line1 = type_ + "\t" + service_id_
    line1 = type_ + "\t" + name_
    my_file.write(line1 + "\n")
    my_file.write(dsp_ + "\n")
    my_file.write(operator_ + "\n")
    #my_file.write(name_ + "\n")
    my_file.write(prod_bp_ + "\n")
    my_file.write("BDC\t\t" + bdc_ + "\n")
    my_file.write("--" + "\n")
    if date_ != "":
        my_file.write(date_ + "\n")
    my_file.write(debit_ + "\n")
    my_file.write(vlan_ + "\n\n")

    my_file.write(site_a_ + "\n")
    my_file.write("POP\t\t\t\n\n\nCPE\t\t\t\n\n\n")

    my_file.write("--[INFO]--\n")
    my_file.write(info_complementaires + "\n\n")
    
    for _ in range(8):
        my_file.write("=" * 80 + '\n\n\n')
    my_file.close()

    print("\nFile out>>\t" + file_name_)
    Mbox(soup, bdc_box, operator_name_, vlan_id, type_, service_id_)
    # Open my_file with notepad.exe
    if OPENFILE == True:
        subprocess.call(['notepad.exe', file_name_])
        #os.system(file_name_)


