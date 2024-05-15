from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

MODEL_NAME = 'Model-1'

CILIUM_RADIUS = 0.12
CILIUM_LENGTH = 10.0

MT_DOUBLET_NUMBER = 9
MT_RADIUS = MT_DOUBLET_NUMBER*[0.01]
#MT_LENGTH_A = MT_DOUBLET_NUMBER*[10.0]
MT_LENGTH_A = [3.83,1.51,1.29,1.19,2.91,2.0,2.07,0.96,1.68]
#MT_LENGTH_B = MT_DOUBLET_NUMBER*[10.0]
MT_LENGTH_B = [3.5,1.57,1.19,1.28,2.05,0.86,1.51,1.00,0.81]
MT_COINCIDENT_RADIUS = 0.01/1.5

MT_RADIAL_DISTANCE = 0.099
MT_TILT_ANGLE = 0.0
MT_ROTATION_ANGLE = 0.0

MESH_CILIUM = 0.02
MESH_MT_HEIGHT = 0.08
MESH_MT_RADIAL = 0.1

CILIUM_DENSITY = 1000.0
CILIUM_ALPHA = 0.5
CILIUM_E1 = 800000.0
CILIUM_E2 = 800000.0
CILIUM_v12 = 0.9978888
CILIUM_G12 = 400000.0
CILIUM_G13 = 4000000.0
CILIUM_G23 = 4000000.0

CILIUM_CAP_E = 10000000000.0
CILIUM_CAP_v = 0.3

MT_DENSITY = 10000.0
MT_ALPHA = 0.5
MT_E1 = 2600000000.0
MT_E2 = 2000000.0
MT_v12 = 0.3
MT_G12 = 7000.0
MT_G13 = 4000000.0
MT_G23 = 4000000.0

CILIUM_THICKNESS = 0.0025
CILLIUM_CAP_THICKNESS = 1.0
MICROTUBULE_THICKNESS = 0.005

TIME_STEP = 500.0

LOADING_VALUE = 5.0 # 0.5. 1.0, 2.5, 5.0
REST_NUMBER = 5
AMPLITUDE = [(0.0, 0.0)]
for i in range(0, 2*REST_NUMBER, 2):
    AMPLITUDE.append((TIME_STEP*(i + 1)/(2*REST_NUMBER), 1.0*(i + 2)/(2*REST_NUMBER)))
    AMPLITUDE.append((TIME_STEP*(i + 2)/(2*REST_NUMBER), 1.0*(i + 2)/(2*REST_NUMBER)))

AMPLITUDE = ((0.0, 0.0), (TIME_STEP/50.0, 1.0), (TIME_STEP, 1.0))
JOB_NAME = "CILIUM_L10_T50"
CPUS = 16


### GENERATING MODEL ##################################################
MODEL = mdb.Model(modelType=STANDARD_EXPLICIT, name=MODEL_NAME)

### GENERATING PARTS ###
## CILIUM PART
MODEL.ConstrainedSketch(name='__profile__', sheetSize=CILIUM_LENGTH*4)
MODEL.sketches['__profile__'].ConstructionLine(point1=(0.0, 
    -CILIUM_LENGTH*2), point2=(0.0, CILIUM_LENGTH*2))
MODEL.sketches['__profile__'].FixedConstraint(entity=
    MODEL.sketches['__profile__'].geometry[2])
    

    
MODEL.sketches['__profile__'].Line(point1=(CILIUM_RADIUS, 0.0), point2=(
    CILIUM_RADIUS, CILIUM_LENGTH))

MODEL.sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=MODEL.sketches['__profile__'].geometry[3])

MODEL.sketches['__profile__'].ArcByCenterEnds(center=(0.0, CILIUM_LENGTH)
    , direction=COUNTERCLOCKWISE, point1=(CILIUM_RADIUS, CILIUM_LENGTH), point2=(0.0, 
    CILIUM_LENGTH + CILIUM_RADIUS))


print(MODEL.sketches['__profile__'].vertices)

MODEL.sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    MODEL.sketches['__profile__'].vertices[2], entity2=
    MODEL.sketches['__profile__'].geometry[2])
MODEL.sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    MODEL.sketches['__profile__'].vertices[3], entity2=
    MODEL.sketches['__profile__'].geometry[2])
    
MODEL.Part(dimensionality=THREE_D, name='PART-CILIUM', type=
    DEFORMABLE_BODY)
MODEL.parts['PART-CILIUM'].BaseShellRevolve(angle=360.0, 
    flipRevolveDirection=OFF, sketch=
    MODEL.sketches['__profile__'])
del MODEL.sketches['__profile__']

## MICROTUBULE PART
for i in range(MT_DOUBLET_NUMBER):

    MODEL.ConstrainedSketch(name='__profile__', sheetSize=0.05)
    MODEL.sketches['__profile__'].CircleByCenterPerimeter(center=(
        0.0, 0.0), point1=(MT_RADIUS[i], 0.0))
    MODEL.Part(dimensionality=THREE_D, name='PART-MT-A-' + str(i + 1), type=
        DEFORMABLE_BODY)
    MODEL.parts['PART-MT-A-' + str(i + 1)].BaseShellExtrude(depth=MT_LENGTH_A[i], sketch=
        MODEL.sketches['__profile__'])
    del MODEL.sketches['__profile__']
    
    
    MODEL.ConstrainedSketch(name='__profile__', sheetSize=0.05)
    MODEL.sketches['__profile__'].Arc3Points(point1=(0.0, MT_COINCIDENT_RADIUS), 
        point2=(0.0, -MT_COINCIDENT_RADIUS), point3=((MT_RADIUS[i]**2 - MT_COINCIDENT_RADIUS**2)**0.5 + MT_RADIUS[i], 0.0))
    MODEL.sketches['__profile__'].move(objectList=(
    MODEL.sketches['__profile__'].geometry[2], ), vector=(-(MT_RADIUS[i]**2 - MT_COINCIDENT_RADIUS**2)**0.5, 
    0.0))
    MODEL.Part(dimensionality=THREE_D, name='PART-MT-B-' + str(i + 1), type=
        DEFORMABLE_BODY)
    MODEL.parts['PART-MT-B-' + str(i + 1)].BaseShellExtrude(depth=MT_LENGTH_B[i], sketch=
        MODEL.sketches['__profile__'])
    del MODEL.sketches['__profile__']
    

MODEL.parts['PART-CILIUM'].Set(faces=
    MODEL.parts['PART-CILIUM'].faces.getSequenceFromMask((
    '[#3 ]', ), ), name='SET-WHOLE')
MODEL.parts['PART-CILIUM'].Set(faces=
    MODEL.parts['PART-CILIUM'].faces.getSequenceFromMask((
    '[#2 ]', ), ), name='SET-BODY')
MODEL.parts['PART-CILIUM'].Set(faces=
    MODEL.parts['PART-CILIUM'].faces.getSequenceFromMask((
    '[#1 ]', ), ), name='SET-CAP')
MODEL.parts['PART-CILIUM'].Set(edges=
    MODEL.parts['PART-CILIUM'].edges.getSequenceFromMask((
    '[#8 ]', ), ), name='SET-BASE')
    
for i in range(MT_DOUBLET_NUMBER):
    MODEL.parts['PART-MT-A-' + str(i + 1)].Set(faces=
        MODEL.parts['PART-MT-A-' + str(i + 1)].faces.getSequenceFromMask((
        '[#1 ]', ), ), name='SET-WHOLE')
        
    MODEL.parts['PART-MT-A-' + str(i + 1)].Set(edges=
        MODEL.parts['PART-MT-A-' + str(i + 1)].edges.getSequenceFromMask((
        '[#2 ]', ), ), name='SET-BASE')
    
    MODEL.parts['PART-MT-B-' + str(i + 1)].Set(faces=
        MODEL.parts['PART-MT-B-' + str(i + 1)].faces.getSequenceFromMask((
        '[#1 ]', ), ), name='SET-WHOLE')
        
    MODEL.parts['PART-MT-B-' + str(i + 1)].Set(edges=
        MODEL.parts['PART-MT-B-' + str(i + 1)].edges.getSequenceFromMask((
        '[#4 ]', ), ), name='SET-BASE')
    
    MODEL.parts['PART-MT-A-' + str(i + 1)].DatumCsysByThreePoints(coordSysType=
        CYLINDRICAL, name='Datum csys-1', origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 
        0.0), point2=(1.0, 1.0, 0.0))
    
    MODEL.parts['PART-MT-A-' + str(i + 1)].DatumCsysByThreePoints(coordSysType=
        CYLINDRICAL, name='Datum csys-2', origin=(0.0, 0.0, MT_LENGTH_A[i]), point1=(1.0, 0.0, 
        MT_LENGTH_A[i]), point2=(1.0, 1.0, MT_LENGTH_A[i]))
    
    MODEL.parts['PART-MT-B-' + str(i + 1)].DatumCsysByThreePoints(coordSysType=
        CYLINDRICAL, name='Datum csys-1', origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 
        0.0), point2=(1.0, 1.0, 0.0))
    
    MODEL.parts['PART-MT-B-' + str(i + 1)].DatumCsysByThreePoints(coordSysType=
        CYLINDRICAL, name='Datum csys-2', origin=(0.0, 0.0, MT_LENGTH_B[i]), point1=(1.0, 0.0, 
        MT_LENGTH_B[i]), point2=(1.0, 1.0, MT_LENGTH_B[i]))
    
    MODEL.parts['PART-MT-A-' + str(i + 1)].MaterialOrientation(
        additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
        , axis=AXIS_2, fieldName='', localCsys=
        MODEL.parts['PART-MT-A-' + str(i + 1)].datums[5], orientationType=
        SYSTEM, region=
        MODEL.parts['PART-MT-A-' + str(i + 1)].sets['SET-WHOLE'])
        
    MODEL.parts['PART-MT-B-' + str(i + 1)].MaterialOrientation(
        additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
        , axis=AXIS_2, fieldName='', localCsys=
        MODEL.parts['PART-MT-B-' + str(i + 1)].datums[5], orientationType=
        SYSTEM, region=
        MODEL.parts['PART-MT-B-' + str(i + 1)].sets['SET-WHOLE'])

### MESHING ###########################################################
        
    MODEL.parts['PART-MT-A-' + str(i + 1)].DatumPlaneByPrincipalPlane(offset=
        0.0, principalPlane=XZPLANE)
    
    MODEL.parts['PART-MT-A-' + str(i + 1)].PartitionFaceByDatumPlane(
        datumPlane=MODEL.parts['PART-MT-A-' + str(i + 1)].datums[6], faces=
        MODEL.parts['PART-MT-A-' + str(i + 1)].faces.getSequenceFromMask((
        '[#1 ]', ), ))
        
    MODEL.parts['PART-MT-A-' + str(i + 1)].seedEdgeBySize(constraint=FINER, 
        deviationFactor=0.1, edges=
        MODEL.parts['PART-MT-A-' + str(i + 1)].edges.getSequenceFromMask((
        '[#5 ]', ), ), minSizeFactor=0.1, size=MESH_MT_HEIGHT)
        
    MODEL.parts['PART-MT-B-' + str(i + 1)].seedEdgeBySize(constraint=FINER, 
        deviationFactor=0.1, edges=
        MODEL.parts['PART-MT-B-' + str(i + 1)].edges.getSequenceFromMask((
        '[#a ]', ), ), minSizeFactor=0.1, size=MESH_MT_HEIGHT)

    MODEL.parts['PART-MT-A-' + str(i + 1)].seedPart(deviationFactor=MESH_MT_RADIAL, 
        minSizeFactor=0.1, size=0.01)
        
    MODEL.parts['PART-MT-A-' + str(i + 1)].setMeshControls(elemShape=QUAD, 
        regions=
        MODEL.parts['PART-MT-A-' + str(i + 1)].faces.getSequenceFromMask((
        '[#1 ]', ), ))
    
    MODEL.parts['PART-MT-A-' + str(i + 1)].generateMesh()
    
    MODEL.parts['PART-MT-B-' + str(i + 1)].seedPart(deviationFactor=MESH_MT_RADIAL, 
        minSizeFactor=0.1, size=0.01)
        
    MODEL.parts['PART-MT-B-' + str(i + 1)].setMeshControls(elemShape=QUAD, 
        regions=
        MODEL.parts['PART-MT-B-' + str(i + 1)].faces.getSequenceFromMask((
        '[#1 ]', ), ))
        
    MODEL.parts['PART-MT-B-' + str(i + 1)].generateMesh()



MODEL.parts['PART-CILIUM'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=MESH_CILIUM)
MODEL.parts['PART-CILIUM'].generateMesh()

### MATERIALS #########################################################
## CILIUM MATERIAL
MODEL.Material(name='MATERIAL-CILIUM')
MODEL.materials['MATERIAL-CILIUM'].Density(table=((CILIUM_DENSITY, ), ))
MODEL.materials['MATERIAL-CILIUM'].Damping(alpha=CILIUM_ALPHA)
MODEL.materials['MATERIAL-CILIUM'].Elastic(table=((CILIUM_E1, CILIUM_E2, 
    CILIUM_v12, CILIUM_G12, CILIUM_G13, CILIUM_G23), ), type=LAMINA)
## CILIUM CAP MATERIAL
MODEL.Material(name='Material-CILIUM-CAP')
MODEL.materials['Material-CILIUM-CAP'].Density(table=((CILIUM_DENSITY, ), ))
MODEL.materials['Material-CILIUM-CAP'].Damping(alpha=CILIUM_ALPHA)
MODEL.materials['Material-CILIUM-CAP'].Elastic(table=((CILIUM_CAP_E, CILIUM_CAP_v), 
    ))
## MICROTUBULE MATERIAL
MODEL.Material(name='MATERIAL-MT')
MODEL.materials['MATERIAL-MT'].Density(table=((MT_DENSITY, ), ))
MODEL.materials['MATERIAL-MT'].Damping(alpha=MT_ALPHA)
MODEL.materials['MATERIAL-MT'].Elastic(table=((MT_E1, MT_E2, 
    MT_v12, MT_G12, MT_G13, MT_G23), ), type=LAMINA)

### SECTIONS ##########################################################
## CILIUM SECTION
MODEL.HomogeneousShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=GAUSS, material='MATERIAL-CILIUM', name='SECTION-CILIUM', 
    nodalThicknessField='', numIntPts=3, poissonDefinition=DEFAULT, 
    preIntegrate=OFF, temperature=GRADIENT, thickness=CILIUM_THICKNESS, thicknessField='', 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
## CILIUM CAP SECTION
MODEL.HomogeneousShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=GAUSS, material='MATERIAL-CILIUM-CAP', name='SECTION-CILIUM-CAP', 
    nodalThicknessField='', numIntPts=3, poissonDefinition=DEFAULT, 
    preIntegrate=OFF, temperature=GRADIENT, thickness=CILLIUM_CAP_THICKNESS, thicknessField='', 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
## MICROTUBULE SECTION
MODEL.HomogeneousShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=GAUSS, material='MATERIAL-MT', name='SECTION-MT', 
    nodalThicknessField='', numIntPts=3, poissonDefinition=DEFAULT, 
    preIntegrate=OFF, temperature=GRADIENT, thickness=MICROTUBULE_THICKNESS, thicknessField='', 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)

### SECTION ASSIGNMENT ################################################
## CILIUM SECTION ASSIGNMENT
MODEL.parts['PART-CILIUM'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    MODEL.parts['PART-CILIUM'].sets['SET-BODY'], sectionName=
    'SECTION-CILIUM', thicknessAssignment=FROM_SECTION)
    
## CILIUM CAP SECTION ASSIGNMENT 
MODEL.parts['PART-CILIUM'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    MODEL.parts['PART-CILIUM'].sets['SET-CAP'], sectionName=
    'SECTION-CILIUM-CAP', thicknessAssignment=FROM_SECTION)
    
## MICROTUBULE SECTION ASSIGNMENT
for i in range(MT_DOUBLET_NUMBER):
    MODEL.parts['PART-MT-A-' + str(i + 1)].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        MODEL.parts['PART-MT-A-' + str(i + 1)].sets['SET-WHOLE'], sectionName=
        'SECTION-MT', thicknessAssignment=FROM_SECTION)
    MODEL.parts['PART-MT-B-' + str(i + 1)].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        MODEL.parts['PART-MT-B-' + str(i + 1)].sets['SET-WHOLE'], sectionName=
        'SECTION-MT', thicknessAssignment=FROM_SECTION)    
    
### ASSEMBLY ##########################################################
MODEL.rootAssembly.DatumCsysByDefault(CARTESIAN)
MODEL.rootAssembly.Instance(dependent=ON, name='PART-CILIUM-1', 
    part=MODEL.parts['PART-CILIUM'])
MODEL.rootAssembly.rotate(angle=90.0, axisDirection=(1.0, 0.0, 
        0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('PART-CILIUM-1', ))

BaseLineEdges = MODEL.rootAssembly.instances['PART-CILIUM-1'].edges.getSequenceFromMask(
    mask=('[#8 ]', ), )
      
for i in range(MT_DOUBLET_NUMBER):
    MODEL.rootAssembly.Instance(dependent=ON, name='PART-MT-A-' + str(i + 1) + '-1', 
        part=MODEL.parts['PART-MT-A-' + str(i + 1)])
        
    MODEL.rootAssembly.Instance(dependent=ON, name='PART-MT-B-' + str(i + 1) + '-1', 
        part=MODEL.parts['PART-MT-B-' + str(i + 1)])
    
    MODEL.rootAssembly.translate(instanceList=('PART-MT-A-' + str(i + 1) + '-1', ), 
        vector=(-(MT_RADIUS[i]**2 - MT_COINCIDENT_RADIUS**2)**0.5, 0.0, 0.0))
    
    MODEL.rootAssembly.translate(instanceList=('PART-MT-B-' + str(i + 1) + '-1', ), 
        vector=((MT_RADIUS[i]**2 - MT_COINCIDENT_RADIUS**2)**0.5, 0.0, 0.0))
        
    MODEL.rootAssembly.rotate(angle=MT_TILT_ANGLE, axisDirection=(0.0, 0.0, 
        1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('PART-MT-A-' + str(i + 1) + '-1', ))
    
    MODEL.rootAssembly.rotate(angle=MT_TILT_ANGLE, axisDirection=(0.0, 0.0, 
        1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('PART-MT-B-' + str(i + 1) + '-1', ))
        
    MODEL.rootAssembly.translate(instanceList=('PART-MT-A-' + str(i + 1) + '-1', ), 
        vector=(0.0, MT_RADIAL_DISTANCE, 0.0))
    
    MODEL.rootAssembly.translate(instanceList=('PART-MT-B-' + str(i + 1) + '-1', ), 
        vector=(0.0, MT_RADIAL_DISTANCE, 0.0))
        
    MODEL.rootAssembly.rotate(angle=360.0/MT_DOUBLET_NUMBER*(i - 1) + MT_ROTATION_ANGLE, axisDirection=(0.0, 0.0, 
        1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('PART-MT-A-' + str(i + 1) + '-1', ))
    
    MODEL.rootAssembly.rotate(angle=360.0/MT_DOUBLET_NUMBER*(i - 1) + MT_ROTATION_ANGLE, axisDirection=(0.0, 0.0, 
        1.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('PART-MT-B-' + str(i + 1) + '-1', ))
        
    BaseLineEdges = BaseLineEdges + MODEL.rootAssembly.instances['PART-MT-B-' + str(i + 1) + '-1'].edges.getSequenceFromMask(mask=('[#4 ]', ), )
    BaseLineEdges = BaseLineEdges + MODEL.rootAssembly.instances['PART-MT-A-' + str(i + 1) + '-1'].edges.getSequenceFromMask(mask=('[#18 ]', ), )

MODEL.rootAssembly.Set(edges=BaseLineEdges, name='SET-BASEALL')

## GENERATING SURFACES
MODEL.rootAssembly.Surface(name='Surf-CAP', side1Faces=
    MODEL.rootAssembly.instances['PART-CILIUM-1'].faces.getSequenceFromMask(
    ('[#1 ]', ), ))

for i in range(MT_DOUBLET_NUMBER):
    MODEL.rootAssembly.Surface(name='Surf-A-' + str(i + 1), side12Faces=
        MODEL.rootAssembly.instances['PART-MT-A-' + str(i + 1) + '-1'].faces.getSequenceFromMask(
        ('[#3 ]', ), )) 
    
    MODEL.rootAssembly.Surface(name='Surf-B-' + str(i + 1), side12Faces=
        MODEL.rootAssembly.instances['PART-MT-B-' + str(i + 1) + '-1'].faces.getSequenceFromMask(
        ('[#1 ]', ), ))
              

### STEPS ############################################################# 
MODEL.ExplicitDynamicsStep(improvedDtMethod=ON, name='Step-1', 
    previous='Initial', timePeriod=TIME_STEP)
    
### FIELD OUTPUT ######################################################
MODEL.fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'SVAVG', 'TSHR', 'SSAVG', 'NE', 'LE', 'SE', 'U', 'RF', 'CSTRESS', 
    'CFORCE', 'ENER', 'ELEN', 'ELEDEN', 'EVF', 'STH'))
    
### HISTORY OUTPUT ####################################################
MODEL.historyOutputRequests['H-Output-1'].setValues(variables=(
    'ALLAE', 'ALLIE', 'ALLKE', 'ALLSE', 'ALLVD', 'ALLWK', 'ETOTAL'))
    
    
for i in range(MT_DOUBLET_NUMBER):
    MODEL.HistoryOutputRequest(createStepName='Step-1', name=
        'H-Output-A-' + str(i + 1), rebar=EXCLUDE, region=
        MODEL.rootAssembly.allInstances['PART-MT-A-' + str(i + 1) + '-1'].sets['SET-WHOLE']
        , sectionPoints=DEFAULT, variables=('ALLAE', 'ALLIE', 'ALLKE', 'ALLPD', 
        'ALLSE', 'ALLVD', 'ALLWK', 'ETOTAL'))
        
    MODEL.HistoryOutputRequest(createStepName='Step-1', name=
        'H-Output-B-' + str(i + 1), rebar=EXCLUDE, region=
        MODEL.rootAssembly.allInstances['PART-MT-B-' + str(i + 1) + '-1'].sets['SET-WHOLE']
        , sectionPoints=DEFAULT, variables=('ALLAE', 'ALLIE', 'ALLKE', 'ALLPD', 
        'ALLSE', 'ALLVD', 'ALLWK', 'ETOTAL'))
        
### INTERACTIONS ######################################################
MODEL.ContactProperty('IntProp-1')
MODEL.interactionProperties['IntProp-1'].TangentialBehavior(
    formulation=FRICTIONLESS)
MODEL.interactionProperties['IntProp-1'].NormalBehavior(
    allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
    pressureOverclosure=HARD)
MODEL.ContactExp(createStepName='Step-1', name='Int-1')
MODEL.interactions['Int-1'].includedPairs.setValuesInStep(
    stepName='Step-1', useAllstar=ON)
MODEL.interactions['Int-1'].contactPropertyAssignments.appendInStep(
    assignments=((GLOBAL, SELF, 'IntProp-1'), ), stepName='Step-1')
    
    
### CONSTRAINTS #######################################################
SOLVER_DEFAULT
#NODE_TO_SURFACE
for i in range(MT_DOUBLET_NUMBER):
    MODEL.Tie(adjust=ON, constraintEnforcement=SOLVER_DEFAULT, 
        master=MODEL.rootAssembly.surfaces['Surf-A-' + str(i + 1)], name=
        'Constraint-' + str(i + 1), positionTolerance=0.005, positionToleranceMethod=SPECIFIED, 
        slave=MODEL.rootAssembly.surfaces['Surf-B-' + str(i + 1)], thickness=
        OFF, tieRotations=ON)
        
### LOADING ###########################################################
MODEL.SmoothStepAmplitude(data=AMPLITUDE, name=
    'Amp-1', timeSpan=STEP)
MODEL.SurfaceTraction(amplitude='Amp-1', createStepName=
    'Step-1', directionVector=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)), 
    distributionType=UNIFORM, field='', follower=ON, localCsys=None, 
    magnitude=LOADING_VALUE/(2*3.1415*CILIUM_RADIUS**2), name='Load-1', region=
    MODEL.rootAssembly.surfaces['Surf-CAP'], resultant=ON, 
    traction=GENERAL)
        
### BC ################################################################
MODEL.EncastreBC(createStepName='Step-1', localCsys=None, name=
    'BC-1', region=MODEL.rootAssembly.sets['SET-BASEALL'])


### JOB ###############################################################
mdb.Job(activateLoadBalancing=False, atTime=None, contactPrint=OFF, 
    description='', echoPrint=OFF, explicitPrecision=DOUBLE_PLUS_PACK, 
    historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model=MODEL_NAME, 
    modelPrint=OFF, multiprocessingMode=DEFAULT, name=JOB_NAME, 
    nodalOutputPrecision=SINGLE, numCpus=CPUS, numDomains=CPUS, 
    parallelizationMethodExplicit=DOMAIN, queue=None, resultsFormat=ODB, 
    scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    
mdb.jobs[JOB_NAME].writeInput()