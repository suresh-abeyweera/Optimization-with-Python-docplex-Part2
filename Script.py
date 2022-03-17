import streamlit as st
from docplex.mp.model import Model
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns

st.write("""
# Car Production Planning App

This model is an extension of the https://suresh-abeyweera.medium.com/optimization-with-python-docplex-beginners-guide-d54b77ac715d
  \n This demo shows the integration of Streamlit with docplex


""")

    
image = Image.open('car1.jpg')
st.image(image)

st.sidebar.header('User Input Values')
st.sidebar.write('Select the parameter values')

sidebar_expander_demand = st.sidebar.expander("Car Demand Values")
with sidebar_expander_demand:
    
    selected_carA_lower_bound = st.slider('Minimum Car A Units', 10, 100,10,key = "carA_lower_bound")
    selected_carB_lower_bound = st.slider('Minimum Car B Units', 10, 100,10,key = "carB_lower_bound")

 
sidebar_expander_profit = st.sidebar.expander("Car Profit Values")
with sidebar_expander_profit:
    
    selected_carA_profit = st.slider('Profits by Selling 1 Unit of CarA', 10, 100,12,key = "carA_profit")
    selected_carB_profit = st.slider('Profits by Selling 1 Unit of CarB', 10, 100,15,key = "carB_profit")


sidebar_expander_assembly = st.sidebar.expander("Assembly Time(Days)")
with sidebar_expander_assembly:
    
    selected_carA_assemble_time = st.slider('Days Spent for Assembling 1 Unit of CarA', 0.1, 0.5,0.5,key = "carA_assemble_time")
    selected_carB_assemble_time = st.slider('Days Spent for Assembling 1 Unit of CarB', 0.1, 0.5,0.25,key = "carB_assemble_time")

sidebar_expander_paintfinish = st.sidebar.expander("Painting and Finishing Time(Days)")
with sidebar_expander_paintfinish:
    
    selected_carA_paint_finish_time = st.slider('Days Spent for Assembling 1 Unit of CarA', 0.1, 0.5,0.15,key = "carA_paint_finish_time")
    selected_carB_paint_finish_time = st.slider('Days Spent for Painting and Finishing 1 Unit of CarB', 0.1, 0.5,0.1,key = "carB_paint_finish_time")

sidebar_expander_capacity = st.sidebar.expander("Capacity Constraints")
with sidebar_expander_capacity:
    
    selected_max_capacity_assemblyline = st.slider('Maximum Capacity for Assembly Line', 10, 100,20,key = "max_capacity_assemblyline")
    selected_max_capacity_paintfinishline = st.slider('Maximum Capacity for Painting & Finishing Line', 10, 100,10,key = "max_capacity_paintfinishline")

my_model = Model(name='Car_Production')

CarA = my_model.integer_var(name='CarA')
CarB = my_model.integer_var(name='CarB')


# constraint #1: CarA production is greater than 10
my_model.add_constraint(CarA >= selected_carA_lower_bound)

# constraint #2: CarB production is greater than 10
my_model.add_constraint(CarB >= selected_carB_lower_bound)

import pandas as pd
list_of_lists = []
list_of_lists.append(['CarA',selected_carA_assemble_time,selected_carA_paint_finish_time,selected_carA_lower_bound,selected_carA_profit])
list_of_lists.append(['CarB',selected_carB_assemble_time,selected_carB_paint_finish_time,selected_carB_lower_bound,selected_carB_profit])

df = pd.DataFrame(list_of_lists, columns=['Car Type', 'Days - assemble', 'Days - paint and finish', 'Minimum Production','Profits'])

st.subheader('User Input parameters')
st.write(df)

# constraint #3: Assembly Line has a Maximum Capacity Limitaion
ct_assembly = my_model.add_constraint( selected_carA_assemble_time * CarA + selected_carB_assemble_time * CarB <= selected_max_capacity_assemblyline)

# constraint #4: Painting and Finishing Line has a Maximum Capacity Limitation.
ct_painting = my_model.add_constraint( selected_carA_paint_finish_time * CarA + selected_carB_paint_finish_time * CarB <= selected_max_capacity_paintfinishline)


my_model.maximize(selected_carA_profit * 1000* CarA + selected_carB_profit * 1000 * CarB)



if st.button('Solve Model'):
    
    solution = my_model.solve()

    solve_time = my_model.solve_details.time
    solve_status = my_model.solve_details.status



    print(solution)
    my_model.print_solution()

    st.subheader('Solve Status')
    st.write(solve_status)

    st.subheader('Solve Time')
    st.write("%.5f" % round(solve_time, 5)+ " Seconds")

    if solve_status == "integer optimal solution":
        st.markdown("""<hr style="height:0.1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        carA_solution = solution.get_value(CarA)
        carB_solution = solution.get_value(CarB)
        
        col1.subheader('Car A Production')
        col1.write(str(int(carA_solution)) + " Cars")

        col2.subheader('Car B Production')
        col2.write(str(int(carB_solution))+ " Cars")


        carA_profit_solution = selected_carA_profit * 1000* carA_solution
        carB_profit_solution = selected_carB_profit * 1000* carB_solution
        
        
        solution_lists = []
        solution_lists.append(['CarA',carA_solution,carA_profit_solution,carA_solution * selected_carA_assemble_time, carA_solution * selected_carA_paint_finish_time])
        solution_lists.append(['CarB',carB_solution,carB_profit_solution,carB_solution* selected_carB_assemble_time, carB_solution * selected_carB_paint_finish_time])

        df_solution = pd.DataFrame(solution_lists, columns=["Car Type", "Number of Cars", "Profit" ,"Assembly Time", "Painting & Finishing Time"])
        st.write(df_solution)
        
        
        col1.subheader('Car A Profit')
        col1.write(str(carA_profit_solution)+ " Dollars")

        col2.subheader('Car B Profit')
        col2.write(str(carB_profit_solution)+ " Dollars")
        
        col1.subheader('Number of Cars')
        #col1.bar_chart([carA_solution,carB_solution], width = 1,height=0,use_container_width=True)
        
        x = ['CarA', 'CarB']
        y = [carA_solution, carB_solution]
        fig1 = plt.figure(figsize=(10, 8))
        sns.barplot(x, y)
        col1.pyplot(fig1)
       
        col2.subheader('Total Profit by Car Type')
        labels = 'CarA Profit', 'CarB Profit'
        profit_slutions = [carA_profit_solution, carB_profit_solution]
        explode = (0, 0.1)  

        fig1, ax1 = plt.subplots()
        ax1.pie(profit_slutions, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        col2.pyplot(fig1)
        
        col1.subheader("Capacity Allocation Vs. Usage - Assembling")
        
        x = ['Usage', 'Allocation']
        y = [sum(df_solution["Assembly Time"]), selected_max_capacity_assemblyline]
        fig2 = plt.figure(figsize=(10, 8))
        sns.barplot(x, y)
        col1.pyplot(fig2)
       
        col2.subheader('Capacity Allocation Vs. Usage - Painting & Finishing')
        
        
        x = ['Usage', 'Allocation']
        y = [sum(df_solution["Painting & Finishing Time"]), selected_max_capacity_paintfinishline]
        fig3 = plt.figure(figsize=(10, 8))
        sns.barplot(x, y)
        col2.pyplot(fig3)
        
        st.markdown("""<hr style="height:0.1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.subheader('Optimum Maximum Profit')
        st.write(str(carA_profit_solution + carB_profit_solution)+ " Dollars")
       
    else:
        st.write("Please check the model or check with differernt data set")
         
     
else:
     st.write('Click Solve to generarte the Production plan')
