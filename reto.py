
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

names_link = ('Employees.csv')

@st.cache
def load_data(nrows):
    data =  pd.read_csv(names_link,nrows=nrows)
    data=data.dropna(inplace=False)
    return data

@st.cache
def filter(dtf,fname,variable):
    dtf=dtf[dtf[fname] == variable ]
    return dtf

@st.cache
def filter_text(dtf,fname,variable):
    dtf=dtf[dtf[fname].str.contains(variable)]
    return dtf

############################################################################
st.title("Deserción laboral en empresas y Organizaciones")
st.header('información sobre la Deserción laboral')
st.write("""
En esta pagina encontraras de manera explicativa el fenómeno de 
Deserción laboral obserbando que tanto afecta a las empresas u organizaciones
""")

data_load_state = st.text('Loading data ....')
data = load_data(500)
data_load_state.text("Done! (using st.cache)")
#########################Crear sidebar
sd = st.sidebar
sd.title('Filtro de información')
sd.write("Mostrar u Ocultar Tabla")
#selected_class = sd.radio("Desea mostrar u Ocultar la Tabla", ['Mostrar','Ocultar'])
#sd.write("Selected Class:", selected_class) 
show_hide = sd.checkbox('Ocultar Tabla')

selected_class = sd.radio(" Filtrar por :", ['ID del empleado','Procedencia','Unidad de trabajo'])
myname = sd.text_input('Name: ')
#sd.write("Selected Class:", selected_class) 
selected_Education = sd.selectbox('Filtrado por Nivel de educación',data['Education_Level'].unique())
btnFilter = sd.button('Filtrar Nivel Educativo')
selected_Home = sd.selectbox('Filtrado por Ciudad',data['Hometown'].unique())
btnFilter2 = sd.button('Filtrar Ciudad '+selected_Home)  
selected_Unit = sd.selectbox('Filtrado por Unidad de trabajo',data['Unit'].unique())
btnFilter3 = sd.button('Filtrar '+selected_Unit) 
sd.write("Análisis de Grafico")
show_hist = sd.checkbox('Análisis de Edades')
show_freq = sd.checkbox('Frecuencia por Unidad')
sd.write("Análisis de Deserción")
show_home = sd.checkbox('Ciudad')
show_age = sd.checkbox('Edades')
show_time = sd.checkbox('Tiempo de servicio')

datatem=data

######Mostrar Ocultar dataframe#################
if show_hide:
    st.empty()
    
else:
    
    if (btnFilter):
        datatem = filter(datatem,'Education_Level',selected_Education)
        count_row = datatem.shape[0] # Gives number of rows
        st.write(f'Total de empleados : {count_row}')
    
    if (btnFilter2):
        datatem = filter(datatem,'Hometown',selected_Home)
        count_row = datatem.shape[0] # Gives number of rows
        st.write(f'Total de empleados : {count_row}')
    
    if (btnFilter3):
        datatem = filter(datatem,'Unit',selected_Unit)
        count_row = datatem.shape[0] # Gives number of rows
        st.write(f'Total de empleados : {count_row}')
    
    if (myname):
        if selected_class == 'ID del empleado':
            filterbyname= filter_text(datatem,'Employee_ID',myname)
            count_row = filterbyname.shape[0] # Gives number of rows
            st.write(f'Total names: {count_row}')
            st.empty()
            datatem=filterbyname
        elif selected_class == 'Procedencia':
            filterbyname= filter_text(datatem,'Hometown',myname)
            count_row = filterbyname.shape[0] # Gives number of rows
            st.write(f'Total names: {count_row}')
            st.empty()
            datatem=filterbyname
        
        elif selected_class == 'Unidad de trabajo':
            filterbyname= filter_text(datatem,'Unit',myname)
            count_row = filterbyname.shape[0] # Gives number of rows
            st.write(f'Total names: {count_row}')
            datatem=filterbyname
            st.empty()
        
        
        

    st.dataframe(datatem)
    
###################################################

####################################Filtro###############
if show_hist:

    fig, ax = plt.subplots()
    v,m,g=ax.hist(data ['Age'],bins = range(19, 65 + 2),color='#0BD4B2')
    plt.ylabel('Frecuencia')
    plt.xlabel('Edades')
    plt.title('Histograma de edades')
    plt.yticks(range(0,25,5))
    plt.grid(True)
    st.pyplot(fig)

else:
    st.empty()
if show_freq:
    fig, ax = plt.subplots()
    v,m,g=ax.hist(data ['Unit'],bins = range(0, 12 + 2),color='#8D2AEA')
    plt.ylabel('Frecuencia')
    plt.xlabel('Unidad funcional')
    plt.title('Histograma de Unidades Funcionales')
    plt.yticks(range(0,100,20))
    plt.xticks(rotation =90)
    plt.grid(True)
    st.pyplot(fig)
else:
    st.empty()
    
if show_home:
    data1=data[['Hometown','Attrition_rate']]
    data1=data1.groupby('Hometown',as_index=False).mean()
    x_pos=data1['Hometown']
    y_pos=data1['Attrition_rate']
    fig, ax = plt.subplots()
    ax.bar(x_pos,y_pos,color='#E34F13')
    plt.ylabel('índice de deserción')
    plt.xlabel('Ciudades')
    plt.title('Análisis de deserción por Ciudades')
    plt.xticks(rotation =90)
    plt.grid(True)
    st.pyplot(fig)

else:
    st.empty()
    
if show_age:
    data1=data[['Age','Attrition_rate']]
    data1=data1.groupby('Age',as_index=False).mean()
    x_pos=data1['Age']
    y_pos=data1['Attrition_rate']
    fig, ax = plt.subplots()
    ax.bar(x_pos,y_pos,color='#6355C6')
    plt.ylabel('Indice de deserción')
    plt.xlabel('Edades')
    plt.title('Análisis de deserción por Ciudades')
    plt.xticks(range(18,70,3),rotation =90)
    plt.grid(True)
    st.pyplot(fig)
    
else:
    st.empty()

if show_time:

    data1=data[['Time_of_service','Attrition_rate']]
    data1=data1.groupby('Time_of_service',as_index=False).mean()
    x_pos=data1['Time_of_service']
    y_pos=data1['Attrition_rate']
    fig, ax = plt.subplots()
    ax.bar(x_pos,y_pos,color='#83D02C')
    plt.ylabel('Indice de deserción')
    plt.xlabel('Tiempo de servicio')
    plt.title('Análisis de deserción por Ciudades')
    plt.xticks(range(0,40,2),rotation =90)
    plt.grid(True)
    st.pyplot(fig)
    
else:
    st.empty()
####################################################################
        

