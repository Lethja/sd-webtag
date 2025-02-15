# SD-Webtag

This project is a web-based application designed to manage image tag sets efficiently using the Gradio framework. 
It provides an intuitive interface to organize, edit, and export tags associated with image files. 
The application is especially useful for categorizing image datasets with custom metadata, 
making it suitable for tasks such as machine learning dataset preparation.

## Features

- **Upload and Import Files**: Easily upload images and text-based tag files for tagging and management.
- **Add and Edit Tags**: Add new tags or edit existing ones via a dynamic tag management interface.
- **Tag Galleries**: Explore image galleries associated with each tag set.
- **Export and Import Tag Sets**:
  - Export complete tag sets as ZIP archives for sharing or reuse.
  - Import existing tag sets or image collections into the application for management.
- **Dynamic Tag Set Management**: 
  - View and switch and create multiple tag sets using the web ui dropdown menu.
  - See all tags in a tag set at a glance and view/edit which ones are applicable to the currently selected image
- **Listening server and Gradio SSH Tunneling Support**:
  - Share your session publicly, locally or keep it private to just one machine.

## Getting Started

### Prerequisites
- Python 3.8 or higher (Windows 7 should be supported)
- Pip

### Installation

#### Using a Virtual Environment (optional, but highly recommended)
It is highly recommended to use a Python virtual environment (`venv`) 
to isolate dependencies for this project and avoid potential conflicts with system-wide Python libraries 
and/or other Python projects.

##### Create a virtual environment:
In a terminal with the working directory set to the repository root, 
run the following command to setup a python virtual environment in a new folder called `venv`:
   ```bash
   python3 -m venv venv
   ```
##### Activate the virtual environment
To activate the virtual environment in this terminal you need to run the `venv/bin/activate` script which will set pythons libraries variables away from the system ones and to the `venv` path instead. 
###### POSIX (BSD/Linux/macOS etc...)
```bash
source venv/bin/activate
```
###### CMD (Windows NT6+)
```cmd
.\venv\Scripts\activate
```

When activated, the shell prompt will contain "(venv)" to indicate you're in the python virtual environment in this terminal.

> Note: you can deactivate the virtual environment at anytime by running `deactivate`

##### Install dependencies in the virtual environment
```bash
pip install -r requirements.txt
```

### Running the Application
#### Start the server
[Activate the virtual environment](#activate-the-virtual-environment) in your terminal if you haven't already
then write the following:
```bash
python3 main.py
```
Append the following options as needed and then press enter to run:
- `--path`: Specify a custom directory to store images and tags.
  - If none is specified, a directory named `Sets` will be used. 
  - If the folder doesn't exist it will be created.
- `--zip`: Specify a custom output directory for ZIP exports. 
  - If none is specified, a directory named `Zips` will be used. 
  - If the folder doesn't exist it will be created.
- `--listen`: Make the server globally accessible within the same network (useful for local sharing).
  - In a typical home network environment, a home routers [NAT](https://en.wikipedia.org/wiki/Network_address_translation) will prevent access to this server from the Internet but allow access to any other machines in the same subnet.
  - In a typical cloud hosting environment at least one network interface will be given a public IP which could result in strangers connecting to the server. Use this option with caution in these environments. 
- `--share`: Enable SSH tunneling to share the app via an external [Gradio link](https://gradio.app).
  - If you want to share your instance 

> Tip: It may be more convenient to write your own launcher script than repeating these steps each time \
> \
> POSIX Bash Example:
> ```bash
> #/bin/bash
> . venv/bin/activate
> python3 main.py --path ~/Pictures/Sets --zip /tmp/Zips --listen
> ```
> \
> NT Batch Example:
> ```bat
> venv/bin/activate
> python3 main.py --path %USERPROFILE%\Pictures\Sets --zip %TEMP%\Zips --listen
> ```

##### Connecting to the interface
Access the UI with a web browser at:
```
http://127.0.0.1:7860
```
> Tip: If `--listen` is used, the web interface will be accessible from every IPv4 address this device has assigned to it. \
> \
> For example: say local url is reported as `http://0.0.0.0:7860` 
> on a device that has an ethernet card assigned to `192.168.1.2` and a Wi-Fi card assigned `10.0.0.10`.
> This means the web interface will be accessible from the following addresses:
> - `http://10.0.0.10:7860`
> - `http://127.0.0.1:7860` 
>   - Only accessible from the same device
> - `http://192.168.1.2:7860`

#### Using the interface
##### Tag Set
This section contains a dropdown menu sets what tag sets the user should work on.

Tag Sets are a useful way to categorize image tagging by a common theme or trend
(such as a character, fictional universe, action or art style) 
and allow for completely incompatible sets of images and tags to be segregated yet worked on at the same time. 

To switch what Tag Set is active select one from dropdown menu. 
You can also type the name of a Tag Set, if it does not exist it will be created.

When not needed, Tag Set section can be collapsed with the little arrow to the right
to give more room for viewing [pictures](#pictures) below.

###### Upload/Import
Press this button to bring up a upload dialog. Multiple files can be selected.

When common images formats (`.png`, `.jpeg` etc...) are selected the images are uploaded.
When `.txt` files are uploaded they're considered to be a comma seperated set of tags for the image of the same name.

##### Exports
This section contains options to create and download tag set exports.

When not needed, Exports section can be collapsed with the little arrow to the right
to give more room for viewing [pictures](#pictures) below.

###### Export Tag Set
Press this button to create a zip archives of the currently selected tag set. 
Once completed the zip will appear in the file browser below the button named after the tag set
and date and time the export was requested.

###### Download Export
Press this button to download whatever export is selected in the file browser above.

##### Pictures
This picture galley shows all images in this tag set. 
When an image is selected the tags in the right column will be updated to reflect the state of the tags of that image.

##### Add Tags
This section contains a text field to allow you to set new tags for the image selected in the gallery.

Multiple tags can be typed by separating each with a comma (`,`). 
Press enter to add the tags to the currently selected image.
Adding tags or selecting another image will not clear the text. 
This allows you to add more common tags among all images in a tag set to the left
while appending and removing differences to the right. 

When not needed, Add Tags section can be collapsed with the little arrow to the right
to give more room for [Tags](#tags) below.

##### Tags
This section shows all tags in the selected tag set with the ones applicable to the selected image checked. 
It's possible to check and uncheck any tag in this list to add or remove it from the selected image.

## Future Enhancements
SD-Webtag is currently a work in progress. Future enhancements include: 
- Improve tag conflict resolution when importing files.
- Add functionality for advanced tag search and filtering.
- Enhance the export functionality for individual images or partial datasets.

Happy Tagging