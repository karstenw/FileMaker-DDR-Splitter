# FileMaker-DDR-Splitter

Split a FileMaker Database Design Report into it's components.

The script has been used on OSX with V10 & V11 DDRs. Windows, Linux and DDRV12/13 may or may not work.

## Prerequisites

Python 2.7 - Version 2.5 and 2.6 should work. Version 3.x probably not.



## Usage

```shell
python ddrsplit.py /PATH/TO/Summary.xml
```
This will create a folder named "Exports" at the ```Summary.xml```level.

Inside Exports for each database file this will create a folder with the database name.

Inside the database folder (drumroll) there will be up to 6 subfolders, namely Assets, Basetables, Filereferences, Layouts, Relationships & Scripts.

+ Assets - contains images and other stuff found in layouts. The filename will be it's SHA-1 hexdigest. The file extension is either derived from it's type or .TYPE for unknown types.

+ Basetables - for each basetable there will be it's xml from the DDR. The name pattern is 00000ID_NAME.xml

+ Filereferences - for each basetable there will be it's xml from the DDR. The name pattern is 00000ID_NAME.xml

+ Layouts - for each basetable there will be it's xml from the DDR. The name pattern is 00000ID_NAME.xml.  Folders should be preserved.

+ Relationships - In work. Currently only one XML file for all relationships

+ Scripts - for each basetable there will be it's xml from the DDR. The name pattern is 00000ID_NAME.xml.  Folders should be preserved.