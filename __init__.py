bl_info = {
    "name": "4DSCRIPT",
    "description": "",
    "author": "A_RAPTR",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object" }
import bpy
import bpy.types
from bpy.types import Panel
from bpy.types import Operator
import math 
import bmesh
from mathutils import Vector, Matrix
import copy
#import numpy as np

#HANDLER  #PROPERTY
def handler(self,context):
    bpy.ops.dimension.script()
    
    

def Exec():
    print('')
    print('-------NEW INSTANCE------------')
    
    if not 'Vert' in bpy.data.objects:
        name = "Vert"
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name,mesh)
        col = bpy.context.scene.collection
        col.objects.link(obj)
        bpy.context.view_layer.objects.active= obj
    
    bpy.ops.object.mode_set(mode='OBJECT')
    cameraorigin = bpy.data.objects['Vert']
    projection = cameraorigin.data
    
    dimensions = 4
    
    _4Dverts = [[1,1,1,1],[1,-1,1,1],[1,1,-1,1],[1,1,1,-1],
                [1,-1,-1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,-1],
                [-1,1,1,1],[-1,-1,1,1],[-1,1,-1,1],[-1,1,1,-1],
                [-1,-1,-1,1],[-1,-1,1,-1],[-1,1,-1,-1],[-1,-1,-1,-1]
    
    ]
    #4DORIGN #ORIGIN
    _4Dorigin=bpy.context.scene.a_4Dorigin
    
    #ROTATION
    xy_rotate=bpy.context.scene.xy_rotate
    xz_rotate=bpy.context.scene.xz_rotate
    zy_rotate=bpy.context.scene.zy_rotate
    xw_rotate=bpy.context.scene.xw_rotate
    yw_rotate=bpy.context.scene.yw_rotate
    zw_rotate=bpy.context.scene.zw_rotate
    
    #in 3d we talk about axis of rotation but in actuality we use planes of rotation it just so hapens that in 3d there are 3 ways to rotat and there are 3 axis so they happen to lighn up in 3d
    # WE WANT TO ROTATE IN A COUNTER CLOCKWISE MANNER 
    #RIGHT HAND CORDINATE SYSTEM thumb is z is thumb y is index -x is middle
    #zy---
    for v in range(len(_4Dverts)):
        y = _4Dverts[v][1]
        z = _4Dverts[v][2]
        #y
        _4Dverts[v][1] = round(y*math.cos((zy_rotate))- z*math.sin((zy_rotate)),16)
        #z 
        _4Dverts[v][2] =round(y*math.sin((zy_rotate))+ z*math.cos((zy_rotate)),16)
    
        
    #xz----
    for v in range(len(_4Dverts)):
        x = _4Dverts[v][0]
        z = _4Dverts[v][2]
        #x
        _4Dverts[v][0] = round(x*math.cos((xz_rotate))+ z*math.sin((xz_rotate)),16)
        #y 
        _4Dverts[v][2] =round(-(x*math.sin((xz_rotate)))+ z*math.cos((xz_rotate)),16)
        
    #xy-----
    for v in range(len(_4Dverts)): 
        
        x = _4Dverts[v][0]
        y = _4Dverts[v][1]
        #x
        _4Dverts[v][0] = round(x*math.cos((xy_rotate))- y*math.sin((xy_rotate)),16)
        #y 
        _4Dverts[v][1] =round(x*math.sin((xy_rotate))+ y*math.cos((xy_rotate)),16)
        
    #xw-----
    for v in range(len(_4Dverts)): 
        
        x = _4Dverts[v][0]
        y = _4Dverts[v][3]
        #x
        _4Dverts[v][0] = round(x*math.cos((xw_rotate))- y*math.sin((xw_rotate)),16)
        #y 
        _4Dverts[v][3] =round(x*math.sin((xw_rotate))+ y*math.cos((xw_rotate)),16)
    #yw-----
    for v in range(len(_4Dverts)): 
        
        x = _4Dverts[v][1]
        y = _4Dverts[v][3]
        #x
        _4Dverts[v][1] = round(x*math.cos((yw_rotate))- y*math.sin((yw_rotate)),16)
        #y 
        _4Dverts[v][3] =round(x*math.sin((yw_rotate))+ y*math.cos((yw_rotate)),16)
    #zw-----
    for v in range(len(_4Dverts)): 
        
        x = _4Dverts[v][2]
        y = _4Dverts[v][3]
        #x
        _4Dverts[v][2] = round(x*math.cos((zw_rotate))- y*math.sin((zw_rotate)),16)
        #y 
        _4Dverts[v][3] =round(x*math.sin((zw_rotate))+ y*math.cos((zw_rotate)),16)
        
    if bpy.context.scene.is_4dto3d == True:
        lightsource = bpy.context.scene.lightsource
        for i in range(len(_4Dverts)):
            if lightsource-_4Dverts[i][3] !=0:
                distance= abs(lightsource-_4Dverts[i][3])
                _4Dverts[i][0]=  _4Dverts[i][0]/distance
                _4Dverts[i][1]= _4Dverts[i][1]/distance
                _4Dverts[i][2]= _4Dverts[i][2]/distance
    
    
    for i in range(len(_4Dverts)):
        _4Dverts[i][0]+=_4Dorigin[0]
        _4Dverts[i][1]+=_4Dorigin[1]
        _4Dverts[i][2]+=_4Dorigin[2]
        _4Dverts[i][3]+=_4Dorigin[3]
    #FINISHED APPLYING ROTATION AND TRANSLATION TO WORLD VERTS LOCAL-> WORLD
    
    #!#GRAMSCHMIDT START
    '''
    # use if you want the lookat to be an object
    _4D_origin_displacement=_4Dorigin.copy()
    for i in range(dimensions):
        _4D_origin_displacement[i] = _4D_origin_displacement[i]-_4Dcamera
        pass
    '''
    #TO FIGURE OUT IF THERES AN ERRO JUST ROTATE A NON PROJECTED CUBE AND IF THEIR ARE ANY DISTORTIONS THEIR IS AN ERROR
    
    
    
    lookat = bpy.context.scene.lookat #CONTROLS 2 AXIS UP DOWN LEFT RIGHT #AFFECTS ANYTHING TO DO WITH X XYplane xz plane
    up_vector = bpy.context.scene.up_vector #CONTROLS ROLL #AFFECTS ANYTHING TO DO WITH Z zy plane remember xz is already used by x
    right_vector=bpy.context.scene.right_vector # CONTROLLS anything to do with y but it has already been limited by xy and zy but for 4d this is not the case
    # ar rotation in one plane should not affect orientation in other planes IT HSOULD ONLY EFFECT LENGTH pi/4,0,pi/4 only effects lenght int the xy plane
    _4d_vector=bpy.context.scene.a_4d_vector
    
    #lookat = [math.pi/4,math.pi/4,0,0]
    #lookat = [math.pi/4,0,math.pi/4,0]
    #lookat = [math.pi/4,0,0,math.pi/4]
    #up_vector= [0,0,math.pi/4,math.pi/4]
    #right_vector = [0,math.pi/4,0,math.pi/4]
    '''ROTATING AN OBJECT LOOKAT IS EQUIVLENT TO TRANSLATING ITS ORIGIN BY THIS ROTATIONAL DISPLACEMTN THEN ROTATING THE OBJECT ARROUND ITS ORIGIN THE SAME AMOUNT OF DEGREES AS INPUTED'''
    
    #normalize lookat
    lookat_normalized = []
    for i in range(len(lookat)):
        lookat_normalized.append(lookat[i])
    #lookat_normalized=copy.deepcopy(lookat)
    lookat_length=0
    for cords in lookat :
        lookat_length+= cords**2
    lookat_length = math.sqrt(lookat_length) 
    for i in range(len(lookat)):
        lookat_normalized[i]/=lookat_length
    print('lookat',lookat) 
    print('lookat',lookat_normalized) 
    print('up_vector',up_vector) 
    print('right_vector',right_vector) 
    print('_4d_vector',_4d_vector) 
    # THERES PROBABLY AN ERROR SOME WHER IN HERE
    #!#UPVECTOR
    print()
    #Dotproduct v1 * v2  divide by v1 to get the ammount of v1 parallel to v2 we are pojecting up onto lookat 
    # and finding the parallel vector then subtracting to find the perpendicular vector
    dotproduct=0
    for i in range(dimensions):
        dotproduct += up_vector[i]*lookat[i]
    vector_projection_length = dotproduct/lookat_length #PARALLEL LENGTH TO BE MULTIPLIED BY A UNIT VECTOR
    up_parallel_vector = []
    up_perpendicular_vector = []
    
    for i in range(dimensions) :
        up_parallel_vector.append(vector_projection_length*(lookat_normalized[i]))
        up_perpendicular_vector.append(up_vector[i]-up_parallel_vector[i])
    
    print("Parallel",up_parallel_vector)  
    print("PERPENDICULAR UP VECTOR",up_perpendicular_vector) 
    
    p_length = 0
    for i in range(dimensions):
        p_length+= up_perpendicular_vector[i]**2
    p_length = math.sqrt(p_length)
    for i in range(dimensions):
        up_perpendicular_vector[i]= up_perpendicular_vector[i]/p_length
    print("PERPENDICULAR UP VECTOR NORMALIZED",up_perpendicular_vector)   
    
    #!#RIGHTVECTOR
    print()
    #?# PART 1 LOOKAT COMPARISON RIGHT
    #Dotproduct v1 * v2  divide by v1 to get the ammount of v1 parallel to v2 we are pojecting up onto lookat 
    # and finding the parallel vector then subtracting to find the perpendicular vector
    dotproduct=0
    for i in range(dimensions):
        dotproduct += right_vector[i]*lookat[i]
    vector_projection_length = dotproduct/lookat_length #PARALLEL LENGTH TO BE MULTIPLIED BY A UNIT VECTOR
    right_parallel_vector = []
    right_perpendicular_vector = []
    
    for i in range(dimensions) :
        right_parallel_vector.append(vector_projection_length*(lookat_normalized[i]))
        right_perpendicular_vector.append(right_vector[i]-right_parallel_vector[i])
    
    print("Parallel RIGHT",right_parallel_vector)  
    print("PERPENDICULAR Right VECTOR",right_perpendicular_vector) 
    
    
    #?# PART 2 UPVECTOR COMPARISON RIGHT
    dotproduct=0
    for i in range(dimensions):
        dotproduct += right_perpendicular_vector[i]*up_perpendicular_vector[i]
    print('Dotproduct <RIGHT,UPVECTOR>')
    print(dotproduct)    
    
    vector_projection = dotproduct 
    
    for i in range(dimensions):
        right_parallel_vector[i]=vector_projection*(up_perpendicular_vector[i])
        right_perpendicular_vector[i]=right_perpendicular_vector[i]-right_parallel_vector[i]
        
    print("RIGHT Parallel FROM UP")
    print(right_parallel_vector)  
    
    print("PERPENDICULAR RIGHT VECTOR FROM UP")
    print(right_perpendicular_vector)   
    
    #?# NORMALIZATION
    p_length = 0
    for i in range(dimensions):
        p_length+= right_perpendicular_vector[i]**2
    p_length = math.sqrt(p_length)
    for i in range(dimensions):
        right_perpendicular_vector[i]= right_perpendicular_vector[i]/p_length
    print("PERPENDICULARRIGHT VECTOR NORMALIZED",right_perpendicular_vector)   
    
    
    #!#4DVECTOR
    print()
    #?# PART 1 LOOKAT COMPARISON 4D
    dotproduct=0
    for i in range(dimensions):
        dotproduct += _4d_vector[i]*lookat[i]
    vector_projection_length = dotproduct/lookat_length #PARALLEL LENGTH TO BE MULTIPLIED BY A UNIT VECTOR
    _4d_parallel_vector = []
    _4d_perpendicular_vector = []
    
    for i in range(dimensions) :
        _4d_parallel_vector.append(vector_projection_length*(lookat_normalized[i]))
        _4d_perpendicular_vector.append(_4d_vector[i]-_4d_parallel_vector[i])
    
    print("Parallel  4d",_4d_parallel_vector)  
    print("PERPENDICULAR 4d VECTOR",_4d_perpendicular_vector) 
    
    #?# PART 2 UP VECTOR COMPARISON 4D
    dotproduct=0
    for i in range(dimensions):
        dotproduct += _4d_perpendicular_vector[i]*up_perpendicular_vector[i]
    print('Dotproduct <4d,UPVECTOR>')
    print(dotproduct)    
    
    vector_projection = dotproduct 
    
    for i in range(dimensions):
        _4d_parallel_vector[i]=vector_projection*(up_perpendicular_vector[i])
        _4d_perpendicular_vector[i]=_4d_perpendicular_vector[i]-_4d_parallel_vector[i]
        
    print("4d Parallel FROM UP")
    print(_4d_parallel_vector)  
    
    print("PERPENDICULAR 4d VECTOR FROM UP")
    print(_4d_perpendicular_vector)   
    
    #?# PART 3 RIGHT VECTOR COMPARISON 4D
    dotproduct=0
    for i in range(dimensions):
        dotproduct += _4d_perpendicular_vector[i]*right_perpendicular_vector[i]
    print('Dotproduct <4d,VECTOR Right>')
    print(dotproduct)    
    
    vector_projection = dotproduct 
    
    for i in range(dimensions):
        _4d_parallel_vector[i]=vector_projection*(right_perpendicular_vector[i])
        _4d_perpendicular_vector[i]=_4d_perpendicular_vector[i]-_4d_parallel_vector[i]
        
    print("RIGHT Parallel FROM 4d")
    print(_4d_parallel_vector)  
    
    print("PERPENDICULAR 4d VECTOR FROM UP")
    print(_4d_perpendicular_vector)   
    
    #?# NORMALIZATION
    p_length = 0
    for i in range(dimensions):
        p_length+= _4d_perpendicular_vector[i]**2
    p_length = math.sqrt(p_length)
    for i in range(dimensions):
        _4d_perpendicular_vector[i]= _4d_perpendicular_vector[i]/p_length
    print("PERPENDICULAR 4D VECTOR NORMALIZED",_4d_perpendicular_vector)  
    
    #!# APPPLY ROTATION
    _4Dcamera=bpy.context.scene.a_4DCamera
    _4D_Vert_displacement=copy.deepcopy(_4Dverts)
    
    for i in range(len(_4Dverts)):
        _4D_Vert_displacement[i][0]=_4Dverts[i][0] - _4Dcamera[0]
        _4D_Vert_displacement[i][1]=_4Dverts[i][1] - _4Dcamera[1]
        _4D_Vert_displacement[i][2]=_4Dverts[i][2] - _4Dcamera[2]
        _4D_Vert_displacement[i][3]=_4Dverts[i][3] - _4Dcamera[3]
    _4D_Vert_camera_position =copy.deepcopy(_4D_Vert_displacement)
    #print(up_perpendicular_vector)
    #HERE I MADE A MISTAKE WERE I FORGOT THE CAMERA POSITION HAD TO USE A SEPRATE LIST WHEN MULTIPLYING BECAUSE 
    #IE_4D_Vert_camera_position[i][0] = _4D_Vert_displacement[i][0]*lookat_normalized[0]+ IS CORRECT BUT I REPLACED 
    # _4D_vert displacement with _4D_Vert_camera_position which caused compound operations because it was used in operations that involved itself, instead of using the orginal unmodified vertices
    for i in range(len(_4D_Vert_camera_position)):
    
        _4D_Vert_camera_position[i][0] =(
        _4D_Vert_displacement[i][0]*lookat_normalized[0]+
        _4D_Vert_displacement[i][1]*lookat_normalized[1]+
        _4D_Vert_displacement[i][2]*lookat_normalized[2]+
        _4D_Vert_displacement[i][3]*lookat_normalized[3]
        )
                                           
        _4D_Vert_camera_position[i][1] = (
        _4D_Vert_displacement[i][0]*right_perpendicular_vector[0]+
        _4D_Vert_displacement[i][1]*right_perpendicular_vector[1]+
        _4D_Vert_displacement[i][2]*right_perpendicular_vector[2]+
        _4D_Vert_displacement[i][3]*right_perpendicular_vector[3]
        )
                                           
        _4D_Vert_camera_position[i][2] = (
        _4D_Vert_displacement[i][0]*up_perpendicular_vector[0]+
        _4D_Vert_displacement[i][1]*up_perpendicular_vector[1]+
        _4D_Vert_displacement[i][2]*up_perpendicular_vector[2]+
        _4D_Vert_displacement[i][3]*up_perpendicular_vector[3]
        )
        _4D_Vert_camera_position[i][3] = (
        _4D_Vert_displacement[i][0]*_4d_perpendicular_vector[0]+
        _4D_Vert_displacement[i][1]*_4d_perpendicular_vector[1]+
        _4D_Vert_displacement[i][2]*_4d_perpendicular_vector[2]+
        _4D_Vert_displacement[i][3]*_4d_perpendicular_vector[3]
        )
    for v in range(len(_4D_Vert_camera_position)):
        print(_4D_Vert_camera_position[v])
    #!#RENDERING    
    bm = bmesh.new()
    bm.from_mesh(projection)
    _4Dverts_converted = copy.deepcopy(_4D_Vert_camera_position)
    fov = bpy.context.scene.fov

    #4D PROJECTION
    
    if  (not bpy.context.scene.is_4dto3d) and bpy.context.scene.is_4dto2d:
        for i in range(len(_4Dverts_converted)):
        
            #YZ SCALE
            
            _4Dverts_converted[i][1]/= abs((math.tan(fov/2))*_4Dverts_converted[i][3])+1
            _4Dverts_converted[i][2]/= abs((math.tan(fov/2))*_4Dverts_converted[i][3])+1
        
            #xSCALE
            
            #_4Dverts_converted[i][0]*= abs(_4Dverts_converted[i][3])+1
            #_4Dverts_converted[i][0]*= abs((math.tan(fov/2))*_4Dverts_converted[i][3])+1
            #_4Dverts_converted[i][0]/= abs((math.tan(fov/2))*_4Dverts_converted[i][3])
            

            
            # IT DOESNT REALLY MAKE SENSE TO USE THESE NOW THAT WE KJNOW ITS EQUIVLENT TO 90 DEGREES ITS BASICALLY MEAININGLESS
            # _4Dverts_converted[i][1]/= abs(_4Dverts_converted[i][3])+1
            # _4Dverts_converted[i][2]/= abs(_4Dverts_converted[i][3])+1
            
            #_4Dverts_converted[i].pop()
    if bpy.context.scene.is_3dto2d:
        for i in range(len(_4Dverts_converted)):
            #_4Dverts_converted[i][0]/= (math.tan(fov/2))*_4Dverts_converted[i][3]+1
            _4Dverts_converted[i][1]/= (math.tan(fov/2))*_4Dverts_converted[i][3]+1
            _4Dverts_converted[i][2]=0
    
    #3DPROJECTION
    if  bpy.context.scene.flaten and not bpy.context.scene.proj3d:
        for i in range(len(_4Dverts_converted)):
            
            #Standard
            _4Dverts_converted[i][1]/= (math.tan(fov/2))*_4Dverts_converted[i][0]
            _4Dverts_converted[i][2]/= (math.tan(fov/2))*_4Dverts_converted[i][0]
            #ABS
            #_4Dverts_converted[i][1]/= abs((math.tan(fov/2))*_4Dverts_converted[i][0])
            #_4Dverts_converted[i][2]/= abs((math.tan(fov/2))*_4Dverts_converted[i][0])
            #not useful equivlent to 90
            #_4Dverts_converted[i][1]/= _4Dverts_converted[i][0]
            #_4Dverts_converted[i][2]/= _4Dverts_converted[i][0]
            
            #downwards
            
            #_4Dverts_converted[i][1]/= abs((math.tan(fov/2))*_4Dverts_converted[i][2]) +1
            #_4Dverts_converted[i][2]=0
            #_4Dverts_converted[i][1]/= (math.tan(fov/2))*_4Dverts_converted[i][0]
            
    if bpy.context.scene.proj3d:
        closebound = 500
        for i in range(len(_4Dverts_converted)):
            if _4Dverts_converted[i][0]<closebound:
                closebound =_4Dverts_converted[i][0]
            
            #if _4Dverts_converted[i][0]-_4Dcamera[0]< closebound
        for i in range(len(_4Dverts_converted)):
            #JUST FOR DEMO ONLY DISTANCE 6
            #Standard
            if not bpy.context.scene.flaten:
                _4Dverts_converted[i][1]=( _4Dverts_converted[i][1])/((math.tan(fov/2))*(_4Dverts_converted[i][0]-closebound+1/math.tan(fov/2)))
                _4Dverts_converted[i][2]= (_4Dverts_converted[i][2])/((math.tan(fov/2))*(_4Dverts_converted[i][0]-closebound+1/math.tan(fov/2)))
            else: 
                _4Dverts_converted[i][1]/= (math.tan(fov/2))*_4Dverts_converted[i][0]
                _4Dverts_converted[i][2]/= (math.tan(fov/2))*_4Dverts_converted[i][0]
            
            
    #FLATEN
    if bpy.context.scene.flaten:
        for i in range(len(_4Dverts_converted)):
            _4Dverts_converted[i][0]=1/math.tan(fov/2)
        
    
    for i in range(len(_4Dverts_converted)):
        _4Dverts_converted[i].pop()
    
    
    # VERTS
    remaining_vert=len(_4Dverts_converted)-len(projection.vertices)
    for i in range(remaining_vert):
        bm.verts.new(_4Dverts_converted[i])
    bm.verts.ensure_lookup_table()
    for i in range(len(_4Dverts_converted)):
        bm.verts[i].co=_4Dverts_converted[i]
        #bm.verts[i].co[0] =_4Dverts_converted[i][0]
        #bm.verts[i].co[1] =_4Dverts_converted[i][1]
        #bm.verts[i].co[2] =_4Dverts_converted[i][2]
    
    #EDGES
    bm.verts.ensure_lookup_table()
    try:bm.edges.new((bm.verts[0],bm.verts[1])) 
    except:pass
    try:bm.edges.new((bm.verts[0],bm.verts[2])) #FRONT BOTTOM RIGHT TO BOTTOM LEFT
    except:pass
    try:bm.edges.new((bm.verts[2],bm.verts[4]))
    except:pass
    try:bm.edges.new((bm.verts[1],bm.verts[4])) #FRONT TOP LEFT TO BOTTOM LEFT
    except:pass
    
    try:bm.edges.new((bm.verts[1],bm.verts[9]))
    except:pass
    try:bm.edges.new((bm.verts[0],bm.verts[8]))
    except:pass
    try:bm.edges.new((bm.verts[2],bm.verts[10]))
    except:pass
    try:bm.edges.new((bm.verts[4],bm.verts[12]))
    except:pass
    
    try:bm.edges.new((bm.verts[9],bm.verts[8]))
    except:pass
    try:bm.edges.new((bm.verts[12],bm.verts[10]))
    except:pass
    try:bm.edges.new((bm.verts[8],bm.verts[10]))
    except:pass
    try:bm.edges.new((bm.verts[9],bm.verts[12]))
    except:pass
    
    try:bm.edges.new((bm.verts[1],bm.verts[5]))
    except:pass
    try:bm.edges.new((bm.verts[0],bm.verts[3]))
    except:pass
    try:bm.edges.new((bm.verts[2],bm.verts[6]))
    except:pass
    try:bm.edges.new((bm.verts[4],bm.verts[7]))
    except:pass
    
    try:bm.edges.new((bm.verts[8],bm.verts[11]))
    except:pass
    try:bm.edges.new((bm.verts[9],bm.verts[13]))
    except:pass
    try:bm.edges.new((bm.verts[12],bm.verts[15]))
    except:pass
    try:bm.edges.new((bm.verts[10],bm.verts[14]))
    except:pass
    
    try:bm.edges.new((bm.verts[11],bm.verts[14]))
    except:pass
    try:bm.edges.new((bm.verts[14],bm.verts[15]))
    except:pass
    try:bm.edges.new((bm.verts[15],bm.verts[13]))
    except:pass
    try:bm.edges.new((bm.verts[13],bm.verts[11]))
    except:pass
    
    try:bm.edges.new((bm.verts[11],bm.verts[3]))
    except:pass
    try:bm.edges.new((bm.verts[13],bm.verts[5]))
    except:pass
    try:bm.edges.new((bm.verts[14],bm.verts[6]))
    except:pass
    try:bm.edges.new((bm.verts[15],bm.verts[7]))
    except:pass
    
    try:bm.edges.new((bm.verts[5],bm.verts[3]))
    except:pass
    try:bm.edges.new((bm.verts[3],bm.verts[6]))
    except:pass
    try:bm.edges.new((bm.verts[6],bm.verts[7]))
    except:pass
    try:bm.edges.new((bm.verts[7],bm.verts[5]))
    except:pass
    
    bm.to_mesh(projection)
    
    #MESHMUSTBE IN EDIT MODE IF YOU WANT TO USE THIS
    #bmesh.update_edit_mesh(projection)
    
    bm.free
    return 1.0
    
    
#?OPERATORS-----------------
#OPERATOR #CLASS
class MESH_OT_do_stuff(Operator): # creates a class that inherits from bpy.types.Operator, operator inherits from bpy.types
    bl_idname = "dimension.script" #for some reason you must have a . in the bl_idname
    bl_label = "4D SCRIPT" 
    bl_description = "backs up the currently selected objects"
    bl_options = {'REGISTER','UNDO'}


    def execute(self, context): # defines a method of the simple operator named execute w
        # THIS WILL BASICALLY PUT AN IMAGE  ONTO THE VERTEX POSITON IT WILL NOT BE ROTATED TO FACE THOUGH I MAY DO THAT LATER
        Exec()
        

        return {'FINISHED'}

#? PANEL-------------------------

class UI_PT_panel2(Panel):  
    bl_space_type = "VIEW_3D" # defines where the panel is created
    bl_region_type = "UI" # what tYpe of panel it is
    bl_label = "4D"
    bl_category = "RUTIL"



    def draw(self, context):
        layout = self.layout
        
        layout.prop(bpy.context.scene,"fov")
        layout.prop(bpy.context.scene,"is_4dto2d")
        layout.prop(bpy.context.scene,"is_4dto3d")
        layout.prop(bpy.context.scene,"lightsource")
        layout.prop(bpy.context.scene,"proj3d")
        layout.prop(bpy.context.scene,"flaten")
        layout.separator()
        
        layout.prop(bpy.context.scene,"is_3dto2d")
        layout.prop(bpy.context.scene,"proj3d")
        layout.prop(bpy.context.scene,"flaten")
        
        layout.separator()
        
        layout.prop(bpy.context.scene,"xy_rotate")
        layout.prop(bpy.context.scene,"xz_rotate")
        layout.prop(bpy.context.scene,"zy_rotate")
        layout.separator()
        
        layout.prop(bpy.context.scene,"xw_rotate")
        layout.prop(bpy.context.scene,"yw_rotate")
        layout.prop(bpy.context.scene,"zw_rotate")
        layout.use_property_split = True
        layout.prop(bpy.context.scene,"a_4Dorigin")
        layout.prop(bpy.context.scene,"a_4DCamera")
        layout.prop(bpy.context.scene,"lookat")
        layout.prop(bpy.context.scene,"up_vector")
        layout.prop(bpy.context.scene,"right_vector")
        layout.prop(bpy.context.scene,"a_4d_vector")
        layout.separator()
        

        #layout.prop(bpy.context.scene,"is_3dto2d")





#KEYMAPS
addon_keymaps=[] # the reason for this is not to register them but to unregister them when addon is disabled
def keyconfig():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:  
        km=kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = []
    
            
        kmi = [
        
        km.keymap_items.new("dimension.script", type='Q', value='PRESS', shift=False,ctrl=True,alt=True,oskey=True)
        
    
        ]
        
        
        for keys in kmi:
            addon_keymaps.append((km,keys))
def removekeyconfig():
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        addon_keymaps.clear()

#REGISTER #PROPERTIES
classes = (MESH_OT_do_stuff,UI_PT_panel2) # defines a new class that inherits from simple operator and simple panel

def register(): # a function named register that goes through the classes defined by classes and registers each might be able to be named anything
    for c in classes: # for loop iterates through the classes
        bpy.utils.register_class(c) #for each stage calles a a method form bpy.utils
    keyconfig()
    bpy.types.Scene.xy_rotate=bpy.props.FloatProperty(name="xy_rotate",update=handler)
    bpy.types.Scene.xz_rotate=bpy.props.FloatProperty(name="xz_rotate",update=handler)
    bpy.types.Scene.zy_rotate=bpy.props.FloatProperty(name="zy_rotate",update=handler)
    
    bpy.types.Scene.xw_rotate=bpy.props.FloatProperty(name="xw_rotate",update=handler)
    bpy.types.Scene.yw_rotate=bpy.props.FloatProperty(name="yw_rotate",update=handler)
    bpy.types.Scene.zw_rotate=bpy.props.FloatProperty(name="zw_rotate",update=handler)
    
    bpy.types.Scene.a_4Dorigin=bpy.props.FloatVectorProperty(name="4Dorigin",default=(6.0, 0.0, 0.0, 1.0),size=4,update=handler)
    bpy.types.Scene.a_4DCamera=bpy.props.FloatVectorProperty(name="4DCamera",default=(0.0, 0.0, 0.0, 0.0),size=4,update=handler)
    bpy.types.Scene.lookat = bpy.props.FloatVectorProperty(name="lookat",default=(1.0, 0.0, 0.0, 0.0),size=4,update=handler)
    bpy.types.Scene.up_vector =bpy.props.FloatVectorProperty(name="up_vector",default=(0.0, 0.0, 1.0, 0.0),size=4,update=handler)
    bpy.types.Scene.right_vector=bpy.props.FloatVectorProperty(name="right_vector",default=(0.0, 1.0, 0.0, 0.0),size=4,update=handler)
    bpy.types.Scene.a_4d_vector=bpy.props.FloatVectorProperty(name="4d_vector",default=(0.0, 0.0, 0.0, 1.0),size=4,update=handler)
    
    bpy.types.Scene.fov =bpy.props.FloatProperty(name="fov",default=math.pi/4,update=handler)
    #bpy.types.Scene.is_4dto2d = bpy.props.BoolProperty(name='4dto2d',update=handler) # 4d to 2d camera
    bpy.types.Scene.is_4dto3d = bpy.props.BoolProperty(name='4dto3d',update=handler) #standard way 4d to 3d
    bpy.types.Scene.lightsource= bpy.props.FloatProperty(name="lightsource",default=-2,update=handler,)
    bpy.types.Scene.proj3d = bpy.props.BoolProperty(name='proj3d',default=False, update=handler)
    bpy.types.Scene.flaten = bpy.props.BoolProperty(name='flaten',default=False, update=handler)
    bpy.types.Scene.is_3dto2d = bpy.props.BoolProperty(name='3dto2d',update=handler) #normal
    bpy.types.Scene.is_4dto2d = bpy.props.BoolProperty(name='4dto2d',default=True, update=handler)
    bpy.types.Scene.is_animate = bpy.props.BoolProperty(name='Animate',default=True, )
    #
    bpy.app.handlers.frame_change_pre.append(handler)
    
    
    ##lights source is just 90 fov perspective projection
    ##is_adjusted = True # this is if you want pure decrease range from 1 infinity or 0 infinity
    


def unregister(): # does the same 
    for c in classes:
       bpy.utils.unregister_class(c)
    removekeyconfig()
    del bpy.types.Scene.xy_rotate
    bpy.app.handlers.frame_change_pre.remove(handler)

#APPHANDLER
