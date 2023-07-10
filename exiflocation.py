import PySimpleGUI as sg
from exif import Image
import webbrowser
import os
import sys

longitude=""
latitude=""
layout = [ [sg.Text("Choose a file: "), sg.InputText() ,sg.FileBrowse()],
           [sg.Button("display image"),sg.Button("extract location")]
          ]


window = sg.Window('image location extractor', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        sys.exit()

    elif event == 'extract location':
        try:
            with open(values[0], 'rb') as image_file:
                my_image = Image(image_file)
                if my_image.has_exif:
                    latitude=my_image.gps_latitude
                    longitude=my_image.gps_longitude
                    converted_latitude= latitude[0] + (float(latitude[1])/60) + (float(latitude[2])/3600)
                    converted_longitude= longitude[0] + (float(longitude[1])/60) + (float(longitude[2])/3600)
                    if my_image.gps_latitude_ref=="N" and my_image.gps_longitude_ref == "W" :
                        webbrowser.open_new_tab(f"https://www.google.com/maps/place/{converted_latitude},-{converted_longitude}")
                    elif my_image.gps_latitude_ref=="S" and my_image.gps_longitude_ref == "E":
                        webbrowser.open_new_tab(f"https://www.google.com/maps/place/-{converted_latitude},{converted_longitude}")
                    elif my_image.gps_latitude_ref=="N" and my_image.gps_longitude_ref == "E":
                        webbrowser.open_new_tab(f"https://www.google.com/maps/place/{converted_latitude},{converted_longitude}")
                    else:
                        webbrowser.open_new_tab(f"https://www.google.com/maps/place/-{converted_latitude},-{converted_longitude}")
                    sg.popup("location was found, opening in browser...")
                else:
                    sg.popup("no location data was found")
        except:
            sg.Popup('Could not open location, file propably doesnt have exif data')

