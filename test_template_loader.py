from coding.template_loader import TemplateLoader

loader = TemplateLoader()

print(loader.available_templates())

print()

template = loader.load("python")

print(template)

print()

print(loader.get_files("python"))