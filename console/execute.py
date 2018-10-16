import os

def nakalaPush():
    cmd = """
    java -jar  nakala-console.jar -email  william.diakite@gmail.com -inputFolder input/ -outputFolder  output/  -cleanOutput
    """
    os.chdir('console/')
    os.system(cmd)
