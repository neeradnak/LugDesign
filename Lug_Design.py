import streamlit as st
from PIL import Image
import pandas as pd

from PIL import Image
st.set_page_config(page_title="Lifting Lug Design",layout="wide")

col1,col2 = st.columns((2,1))
col1.header("""Lifting Lug Design""")
col1.write('---')
image = Image.open('L&T.png')
image2=Image.open("lug dig.png")

col1.image(image)
col2,image(image2)

st.sidebar.header("Input Data")

def user_input_features():

    mat = st.sidebar.selectbox('Material of Construction of Lug?',  ("SA 516 GR. 70",))
    Ys= st.sidebar.number_input('Yield Strength at Room Temperature( kg/mm² )')
    N = st.sidebar.number_input('Number Of Lugs',value=1,step=1)
    Lb =st.sidebar.number_input('Length Of Bottom Of Lug ( mm )')
    Lc= st.sidebar.number_input('Length Of Lug at Centerline of Hole ( mm )')
    t = st.sidebar.number_input('Thickness of Lug( mm )')
    L= st.sidebar.number_input('Distance of centerline of Hole from bottom of Lug( mm )')
    dh =st.sidebar.number_input('Diameter of Hole of Lug( mm )')
    lf =st.sidebar.number_input('Length of Weld Leg( mm )')
    E= st.sidebar.number_input('Weld Efficiency')
    W =st.sidebar.number_input('Weight on a Dishend ( Kg )')
    IP =st.sidebar.number_input('Impact factor')
    if st.sidebar.button("Calcuate"):
        Sb= 0.66*Ys
        Ss=0.4*Ys
        St=0.6*Ys
        WI= (W*IP)/N
        As=2*((Lc/2)-(dh/2))*t
        ShearS=WI/As
        At=(Lc-dh)*t
        TensileS=WI/At
        M=WI*L
        I=(t*pow(Lb,3))/12
        Z=I/(Lb/2)
        BendingS=M/Z
        Aw= 2*(Lb+t)*lf*0.707*E
        WeldingS=WI/Aw

        def ShearStress():
            if ShearS < Ss:
                return "Shear Stress Safe"
            else:
                return " Shear Stress Not Safe, Check again"

        def TensileStress():
            if TensileS < St:
                return "Tensile Stress Safe"
            else:
                return " Tensile Stress Not Safe, Check again"

        def BendingStress():
            if BendingS < Sb:
                return "Bending Stress Safe"
            else:
                return " Bending Stress Not Safe, Check again"

        def WeldingStress():
            if WeldingS < Ss:
                return "Welding Stress Safe"
            else:
                return " Welding Stress Not Safe, Check again"

        X = ShearStress()
        Y = TensileStress()
        Z1 = BendingStress()
        P = WeldingStress()

        return [[Sb,Ss,St,WI,As, ShearS,At,TensileS,M,I,Z, BendingS,Aw,WeldingS],[X,Y,Z1,P]]
    return []

names = ["Allowable Stress in Bending", "Allowable Stress in Shear", " Allowable Stress in Tension","Load on each lug"," Shear Area",
         "Shear Stress", "Tensile Area ","Tensile Stress", "Moment", "Moment Of Inertia","Section Modulus", "Bending stress in Weld",
         "Area of Weld", "Welding stress in Weld"]
output = user_input_features()
if output != []:
    data = pd.DataFrame()
    data['Names'] = names.copy()
    data['Values'] = output[0].copy()
    data['Units'] = ["kg/mm²" , "kg/mm²" , "kg/mm²","KG", "mm2","kg/mm²", "mm2","kg/mm²","kg-mm","mm4", "mm3","kg/mm3","mm2","kg/mm²"]
    # data.set_index('Names',inplace = True)
    #col1.write(data.shape)
    #col1.subheader("Load on each lug")
    a,b = col1.columns((1,1))

    a.dataframe(data.iloc[:7,:])
    b.dataframe(data.iloc[7:,:])


    remark = pd.DataFrame()
    remark['Remark'] = output[1].copy()

    #col2.header("""Results""")
    col2.dataframe(remark)

