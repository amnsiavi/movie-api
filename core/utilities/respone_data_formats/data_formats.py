
def FETCH_SUCESS(instance,serializer=False):

    '''
    if using serializer make serializer=true
    
    '''
    if serializer:

        return {'data':instance.data,'sucess':True}
    else:
        return {'data':instance,'sucess':True}
    
def Post_Request_Sucess_MSG():
    return {'msg':'User Created','sucess':True}

def Put_Request_Sucess_MSG():
    return {'msg':'User Updated','sucess':True}

def Delete_Request_Sucess_MSG():
    return {'msg':'User Deleted','sucess':True}

def Patch_Request_Sucess_MSG():
    return {'msg':'User Updated','sucess':True}


def ADMIN_NOT_FOUND():
    return {'msg':'Admin Not Found','sucess':False}

def User_NOT_FOUND():
    return {'msg':'User Not Found','sucess':False}

