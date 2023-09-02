import sys

from pathlib import Path

from normalize import normalize

import shutil

import threading 

import logging


CATEGORIES = {"Audio":['.mp4','.aiff'],
              "Documents":['.doc','.txt','.pdf'],
              "Images": ['.jpg','jpeg'],
               "Archives":['.stem']
               }

def move_file(file:Path,root_dir:Path, categorie:str) ->None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        logging.info(f"Creating directory: {target_dir}")
        target_dir.mkdir()


    file.replace(target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}"))
    logging.info(f"Move file:{file} to {target_dir}")



def get_categories(file:Path)->str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat

    return 'Other'

def sort_folder(path: Path) -> None:
    threads =[]
     
    for item in path.glob("**/*"):
        if item.is_dir():
           #create threads
           thread =threading.Thread(target=process_subdirectory,args=(item, ))
           threads.append(thread)
           thread.start()
    #finish threads
    for thread in threads:
        thread.join()
            
        

def process_subdirectory(subdirectory:Path) -> None:
    for item in subdirectory.glob("*"):
        if item.is_file():
            cat = get_categories(item)
            move_file(item, subdirectory, cat)



def delete_empty_folder(path:Path) ->None:
    for item in path.glob('**/*'):
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir() 

            logging.info(f"Empty folder {item} is deleted")



def unpack_archive(path:Path) ->None:
    destination_dir = path.joinpath("Archives")
    for i in destination_dir.glob('*'):
        shutil.unpack_archive(i,destination_dir.joinpath(i.stem))




def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        logging.error("No path to folder")
        return "No path to folder"
    
    
    if not path.exists():
        logging.error("Folder with path{path} does not exist")
        return "Folder with path{path} does not exist"
    
    logging.basicConfig(level=logging.DEBUG, format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    sort_folder(path)
    delete_empty_folder(path)
    unpack_archive(path)


    return " Everythin is OK "

if __name__ == '__main__':
    print(main())
 