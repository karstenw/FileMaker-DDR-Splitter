# FileMaker-DDR-Splitter

Split a FileMaker Database Design Report into it's components.

The Script has been used with V10 & V11 DDRs. V12 and V13 may or may not work.


## Usage

```shell
python ddrsplit.py /PATH/TO/Summary.xml
```
This will create a folder named "Exports" at the ```Summary.xml```level.

Inside Exports for each database file this will create a folder with the database name.

Inside the database folder (drumroll) there will be up to 6 subfolders, namely Assets, Basetables, Filereferences, Layouts, Relationships & Scripts.

+ Assets - contains images and other stuff found in layouts. The name will be it's SHA-1 hexdigest.

+ Basetables - for each basetable there will be it's xml from the DDR. The name pattern is ID_NAME.xml

+ Filereferences - for each basetable there will be it's xml from the DDR. The name pattern is ID_NAME.xml

+ Layouts - for each basetable there will be it's xml from the DDR. The name pattern is ID_NAME.xml.  Folders should be preserved.

+ Relationships - In work. Currently only one XML file for all relationships

+ Scripts - for each basetable there will be it's xml from the DDR. The name pattern is ID_NAME.xml.  Folders should be preserved.