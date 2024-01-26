# Prisma-SDWAN
Scripts written for Prisma SD-WAN

The main script was built to pull the current state of a tenant so that it can be referenced.

The use case is that for a Prisma SD-WAN eval, it will not be ported to a production environment, so having a capture of the configuration used in the eval might be useful when building out the production environment. 

To get started, just clone this repo to your IDE, then create a cgxauth.py fail based on the cgxauth_example.txt file, then execute main. 

In the main, you can set two varialbes to True or False depending on if you want to print to screen, write to file, or both. You can also set the filename to whatever you like. 

    PRINT = False
    WRITE_TO_FILE = True
    filename = 'prisma_sdwan_eval_' + str(datetime.date.today()) +'.txt'

Report any issues to me and I'll fix, or update and send me pull requests. 
