



import sys

import os
import shutil

# import win32process
# import win32event




def open_md(mk_path,tmp_folder,editor_path,zpath):


    try:

        filename=os.path.basename(mk_path).split('.')[0]

        fsize = os.path.getsize(mk_path)
        print(fsize)


        md_path=os.path.join(tmp_folder, f"{filename}.md")

        if not fsize:



            if not new_md(md_path):return -1


        else:


            extract_mk(mk_path,tmp_folder,zpath)


        if not os.path.exists(md_path):

            print("md文件不存在")
            os.system(editor_path)
            return


        # print(f"d:\\typora\\typora {md_path}")

        os.system(f"{editor_path} {md_path}")

        # handle= win32process.CreateProcess('d:\\typora\\typora.exe', md_path, None , None , 0 ,0 , None , None ,win32process.STARTUPINFO())
        # win32event.WaitForSingleObject(handle,-1)


    except:
        return -1




def new_md(path):
    try:
        os.mknod(path)
        return 0
    except:
        return None



def extract_mk(path,tmp_folder,zpath):


    print (f"{zpath} x {path} -aoa -o{tmp_folder} ")

    os.system(f"{zpath} x {path} -aoa -o{tmp_folder} ")


def compress_mk(mk_path,tmp_folder,zpath):



    print(f"{zpath} u  {mk_path} {tmp_folder}\* ")
    os.system(f"{zpath} u  {mk_path} {tmp_folder}\* ")

def get_input_path():

    if len(sys.argv)<2:
        return None


    filepath = sys.argv[1]

    print('filepath:', filepath)

    abspath = os.path.abspath(filepath)
    print(abspath)


    if os.path.exists(filepath):
        return abspath
    else:
        return None




def mk_tmp_folder():
    import uuid

    uuid = uuid.uuid1()
    print(uuid)

    systmp=os.environ.get('tmp')

    tmpdir = os.path.join(systmp, str(uuid))
    print(tmpdir)
    try:
        os.mkdir(tmpdir)

        return tmpdir

    except:
        return None



def rm_tmp_folder(tmp_folder):

    try:
        shutil.rmtree(tmp_folder)
    except:
        return -1

def get_7z():
    exedir=os.path.split(os.path.realpath(sys.argv[0]))[0]
    path=os.path.join(exedir,"7z.exe")

    return path

def getEditor():

    exedir=os.path.split(os.path.realpath(sys.argv[0]))[0]
    path=os.path.join(exedir,"md_editor.txt")

    if not os.path.exists(path):
        print("未找到md_editor.txt")
        return None
    try:
        f=open(path,'r')
        path=f.readline().strip()
        f.close()
        return path
    except:
        return None
def run():
    # print(1)
    # os.system("pause")



    editor_path=getEditor()
    if not editor_path or not os.path.exists(editor_path):
        print("未设置编辑器")
        return -1
    # print(2)
    # os.system("pause")


    mk_path = get_input_path()
    if not mk_path:
        print("mk文件不存在")
        os.system(editor_path)
        return -1
    # print(3)
    # os.system("pause")


    zpath=get_7z()
    if not os.path.exists(zpath):
        print("7z不存在")
        os.system(editor_path)
        return -1



    tmp_folder=mk_tmp_folder()

    open_md(mk_path,tmp_folder,editor_path,zpath)
    compress_mk(mk_path,tmp_folder,zpath)
    rm_tmp_folder(tmp_folder)

if __name__=="__main__":

    run()



