



import sys

import os
import shutil

# import win32process
# import win32event




def open_md(md_path,editor_path):


    try:
        if not md_path or not os.path.exists(md_path) :

            print("md文件不存在")
            os.system(editor_path)
            return

        print(f'{editor_path} "{md_path}"')
        os.system(f'{editor_path} "{md_path}"')


    except:
        return -1




def new_md(md_path):
    print(md_path)

    try:
        # os.mknod(f'"{path}"')

        f=open(md_path,'w')
        f.close()
        return True
    except:
        return False



def extract_mz(mz_path,tmp_folder,zpath):


    print (f'{zpath} x "{mz_path}" -aoa -o{tmp_folder} ')

    os.system(f'{zpath} x "{mz_path}" -aoa -o{tmp_folder} ')


    return True


def decompress_mz(mz_path,tmp_folder,zpath):


    # fsize = os.path.getsize(mz_path)
    # print(fsize)
    # if not fsize:
    #     return None

    # rlt=extract_mz(mz_path, tmp_folder, zpath)
    # if not rlt:return None


    print (f'{zpath} x "{mz_path}" -aoa -o{tmp_folder} ')

    os.system(f'{zpath} x "{mz_path}" -aoa -o{tmp_folder} ')


    return True


    # filename = os.path.basename(mz_path).split('.')[0]
    # md_path = os.path.join(tmp_folder, f"{filename}.md")
    #
    #
    # return md_path

def compress_mz(mz_path,tmp_folder,zpath):
    

    if os.path.exists(mz_path):

        fsize = os.path.getsize(mz_path)
        if not fsize:
            os.remove(mz_path)

    print(f'{zpath} u  "{mz_path}" {tmp_folder}\* ')
    os.system(f'{zpath} a -tzip -mcu "{mz_path}" {tmp_folder}\* ')

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






def handle_mz(input_path):
    editor_path = getEditor()
    if not editor_path or not os.path.exists(editor_path):
        print("未设置编辑器")
        return -1

    mz_path = input_path#get_input_path()
    if not mz_path:
        print("mz文件不存在")
        os.system(editor_path)
        return -1
    # print(3)
    # os.system("pause")

    zpath = get_7z()
    if not os.path.exists(zpath):
        print("7z不存在")
        os.system(editor_path)
        return -1

    tmp_folder = mk_tmp_folder()



    filename = os.path.basename(mz_path).split('.')[0]
    md_path = os.path.join(tmp_folder, f"{filename}.md")

    rlt=False
    fsize = os.path.getsize(mz_path)
    if fsize==0:
        rlt=new_md(md_path)
    else:
        rlt=decompress_mz(mz_path, tmp_folder, zpath)

    if not rlt:
        print("mdz文件处理失败")
        os.system(editor_path)
        return -1

    open_md(md_path, editor_path)

    md_size = os.path.getsize(md_path)
    if md_size!=0:
        compress_mz(mz_path, tmp_folder, zpath)
    rm_tmp_folder(tmp_folder)


def handle_md(input_path):
    editor_path = getEditor()
    if not editor_path or not os.path.exists(editor_path):
        print("未设置编辑器")
        return -1
    zpath = get_7z()
    if not os.path.exists(zpath):
        print("7z不存在")
        os.system(editor_path)
        return -1
    # tmp_folder = mk_tmp_folder()

    md_path = input_path#get_input_path()

    filename=os.path.basename(md_path).split(".")[0]
    dir=os.path.dirname(md_path)

    asset_path=os.path.join(dir,f"{filename}.assets")

    if not os.path.exists(asset_path):
        open_md(md_path, editor_path)
    else:

        tmp_folder = mk_tmp_folder()

        tar_md_path=    os.path.join(tmp_folder,f"{filename}.md")
        shutil.copyfile(md_path,tar_md_path)
        tar_asset_path=    os.path.join(tmp_folder,f"{filename}.assets")
        shutil.copytree(asset_path, tar_asset_path)



        # md_path = decompress_mz(mz_path, tmp_folder, zpath)
        open_md(tar_md_path, editor_path)

        mz_path=os.path.join(dir,f"{filename}.mdz")

        if os.path.exists(mz_path):##覆盖提醒
            pass

        compress_mz(mz_path, tmp_folder, zpath)
        rm_tmp_folder(tmp_folder)









def run():



    input_path=get_input_path()


    #input_path="E:\笔记文档\GIT\git rm用法.mdz"

    if input_path.endswith("mdz"):
        handle_mz(input_path)
    elif input_path.endswith("md"):
        handle_md(input_path)


if __name__=="__main__":

    run()



