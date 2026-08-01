from coding.code_generator import CodeGenerator

generator = CodeGenerator()

project = generator.generate_project(

    "Create a Python calculator application."

)

print(project)