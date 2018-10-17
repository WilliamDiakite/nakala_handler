import os
from subprocess import Popen, PIPE

def nakalaPush():
    cmd = """
    java --add-modules=java.xml.bind -XX:+IgnoreUnrecognizedVMOptions -jar  nakala-console.jar -email  william.diakite@gmail.com -inputFolder input/ -outputFolder  output/  -cleanOutput
    """

    # change directory to be able to use the command
    os.chdir('console/')

    # Execute command
    print('[ + ] Launching Nakala subprocess\n')
    os.system(cmd)
    print('\n------ done pushing data ------\n')

    # go back to original directory
    os.chdir('../')
