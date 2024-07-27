import dearpygui.dearpygui as dpg



def main():

    dpg.create_context()
    dpg.create_viewport(title='Smart Frequent Vocabulary Card Creator', width=600, height=300)

    with dpg.window(label="Example Window", tag="Primary Window"):
        dpg.add_text("Find the translation for this word:")
        dpg.add_text(word)
        dpg.add_button(label="Save")
        dpg.add_input_text(label="string", default_value="Quick brown fox")
        dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()





# exectute main:
if __name__ == '__main__':
    main()


