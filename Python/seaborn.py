# Create scatter plot
g = sns.relplot(x="weight", 
                y="horsepower", 
                data=mpg,
                kind="scatter")

# Add a title "Car Weight vs. Horsepower"
g.fig.suptitle("Car Weight vs. Horsepower")

# Show plot
plt.show()

# Set the style to "darkgrid"
sns.set_style("darkgrid")

# Set a custom color palette
# Set a custom color palette
sns.set_palette(["#39A7D0", "#36ADA4"])

'''
'''

# Create the box plot of age distribution by gender
sns.catplot(x="Gender", y="Age", 
            data=survey_data, kind="box")

# Show plot
plt.show()

'''
'''

# Create a point plot that uses color to create subgroups
sns.catplot(kind="point",data=student_data,x="romantic",y="absences",hue="school")

# Show plot
plt.show()
