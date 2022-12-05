import sys

import re
import os
import PySimpleGUI as sg
import urllib3
import random
from datetime import datetime as dt
from alma_tools_mod import AlmaTools
from openpyxl import load_workbook
from time import sleep
#to disable warnings verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#setting arrival date
arrival_date = dt.now().strftime("%Y-%m-%dZ")


# spreadsheet_name = "test_sheet.xlsx"


def my_gui(values = None):
	"""
	This function running form in separate window and collect values
	Returns:
		values(dict) - dictionary of form values
	"""

	if not values:
		spreadsheet_name = "test_sheet.xlsx"


	form = sg.FlexForm('xlsx submit form')
	schemes = ["BlueMono","Tan","BluePurple","LightBrown","SystemDefaultForReal","LightBrown18","LightBrown16","LightBrown15","LightBrown14","LightBrown12","LightBrown11","LightBrown10","LightBrown8","LightBrown7","LightBrown6","LightBrown9","LightBrown5","Kayak","Purple","DarkGreen1","DarkGreen2","DarkGreen3","TealMono","Python","LightGrey3","LightGrey6","SendyBeach","BluePurple","DarkTeal7","LightGreen2",'DarkBrown6','Purple','DarkGreen4','DarkTeal7']
	all_schemes = ['Black', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue', 'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue', 'DarkBlue1', 'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17', 'DarkBlue2', 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8', 'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 'DarkBrown7', 'DarkGreen', 'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen6', 'DarkGreen7', 'DarkGrey', 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12', 'DarkGrey13', 'DarkGrey14', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 'DarkGrey8', 'DarkGrey9', 'DarkPurple', 'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5', 'DarkPurple6', 'DarkPurple7', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 'DarkTeal10', 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 'DarkTeal8', 'DarkTeal9', 'Default', 'Default1', 'DefaultNoMoreNagging', 'GrayGrayGray', 'Green', 'GreenMono', 'GreenTan', 'HotDogStand', 'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 'LightBrown', 'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2', 'LightBrown3', 'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7', 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10', 'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7', 'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6', 'LightPurple', 'LightTeal', 'LightYellow', 'Material1', 'Material2', 'NeutralBlue', 'Purple', 'Python', 'Reddit', 'Reds', 'SandyBeach', 'SystemDefault', 'SystemDefault1', 'SystemDefaultForReal', 'Tan', 'TanBlue', 'TealMono', 'Topanga']
	#all_schemes =["LightBlue2",'LightGrey2',"GrayGrayGray","Default1"]
	
	r = random.choice(all_schemes)
	sg.theme(r)


	

	layout = [

			[sg.Text('This app is making items with barcodes from xlsx file.',font = ('Helvetica', 13, 'bold italic'))],
			[sg.Text('Please select your  spreadsheet.',font = ('Helvetica', 13, 'bold italic'))],
			[sg.Text('browse results', size=(30, 1)),sg.FileBrowse('FileBrowse',key='spreadsheet_name')],
			[sg.Checkbox('Try in SANDBOX?', default=False,key='if_sb',font = ('Helvetica', 11, 'bold italic'))],
			[sg.Button("Run!")]

			]
	
	window =sg.Window(f'Item maker ("{r}" theme)', layout, default_element_size=(35, 2))#,background_color='#ACBAAB')
	event,values=window.read()

	return values,window,event


def make_item(mms_id, holding_id, location, copy_id,barcode,key):

	"""Thid function creates item
	Parameters:
		mms_id(str) - Alms mms id
		holding_id(str) - Alma  holding id
		location(str) - location status_code
		copy_id(str) - identification number
		barcode(str) - barcode
		key(str) - "prod"  or "sb" for passing to AlmaTools
	Returns:
		flag(bool) - True if item created and False if Failed

	"""

	my_api = AlmaTools(key)
	print(key)
	if not holding_id and location:
		my_api.get_holdings(mms_id)
		holdings = re.findall(r'<holding_id>(.*?)</holding_id>', my_api.xml_response_data)
		for holding_id in holdings:
			my_api.get_holding(mms_id, holding_id)
			if location in my_api.xml_response_data:
				sg.Print("Holding id: ", holding_id)
				item_data = """
					<item>
					<holding_data>
						<holding_id></holding_id>
						<copy_id></copy_id>
					</holding_data>
					<item_data>
						<is_magnetic>false</is_magnetic>
						<barcode></barcode>
						<physical_material_type desc="Music Score">SCORE</physical_material_type>
						<policy desc="Music Hire">HIRE</policy>
						<enumeration_a></enumeration_a>
						<enumeration_b></enumeration_b>
						<enumeration_c></enumeration_c>
						<chronology_i></chronology_i>
						<chronology_j></chronology_j> 
						<chronology_k></chronology_k>
						<public_note></public_note>
						<receiving_operator>API</receiving_operator>
						<internal_note_1></internal_note_1>
						<description></description>
						</item_data>
					</item>"""
				
				hold_stat = "<holding_id>{}</holding_id>".format(holding_id)
				barcode_stat = "<barcode>{}</barcode>".format(barcode)
				copy_stat = "<copy_id>{}</copy_id>".format(copy_id)
				# arrival_stat =  r'<arrival_date>{}</arrival_date>'.format(arrival_date)
				item_data = item_data.replace("<holding_id></holding_id>",hold_stat).replace("<barcode></barcode>", barcode_stat).replace("<copy_id></copy_id>", copy_stat)#.replace('<arrival_date></arrival_date>',arrival_stat)
				my_api.create_item(mms_id, holding_id, item_data)
				if str(my_api.status_code).startswith("2"):
					item_pid = re.findall(r"<pid>(.*?)</pid>",my_api.xml_response_data)[0]
					sg.Print("Item created: ", item_pid)
					sg.Print("Item PID: ", item_pid)
					with open("item_report_"+arrival_date+".txt","a") as f:
						f.write(mms_id+"|"+holding_id+"|"+item_pid+"\n")
					return True
				else:
					sg.Print("Failed: ")
					sg.Print(my_api.xml_response_data)
					with open("item_report_"+arrival_date+".txt","a") as f:
						f.write(mms_id+"|"+holding_id+"| Failed \n")
					return False





def item_routine():

	"""This function managing process of making item from spreasheet"""


	values = None
	values,window,event = my_gui(values = values)
	if (values["spreadsheet_name"]==""):
		raise IndexError("Please insert input file source")		
	else:
		spreadsheet_name = values["spreadsheet_name"]
		if values["if_sb"]:
			key = "sb"
		else:
			key = "prod"
		wb = load_workbook(spreadsheet_name)
		ws_name = wb.get_sheet_names()[0]
		ws = wb[ws_name]
		for i, row in enumerate(ws.iter_rows()):
			holding = None
			if i>1:
				mms_id = ws["A{}".format(i)].value
				if mms_id:
					barcode = ws["B{}".format(i)].value
					location = ws["D{}".format(i)].value
					copy_id = ws["C{}".format(i)].value
					holding_id  = ws["E{}".format(i)].value
					sg.Print(copy_id)
					sg.Print("Alma MMS ID: ",mms_id)
					make_item(mms_id=mms_id, holding_id = holding_id, location = location, copy_id= copy_id, barcode=barcode, key = key)
	
	sleep(10)
	window.close()


if __name__ == '__main__':

	item_routine()
