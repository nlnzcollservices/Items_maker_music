# Description


# Instructions

```
git clone https://github.com/nlnzcollservices/Items_maker_music

```

Open  alma_tools_mod.py file and insert your production and sandbox Alma API key

Make sure that all requirements are satisvied.

Prepare you xlsx spreadsheet with the test_sheet.xlsx format

Run items_maker.py 

It should produce small GUI screen with one file pick up and one checkbox option.
Pick up your xlsx file. Tick if you are making items in SB.

[example](gui.PNG)

# Further work

Script containns the following template inside . To adjust to other project just modify this template inside of items_maker.py


```


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
</item>

```
