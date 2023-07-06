# import TKinterModernThemes.examples.allwidgets as allwidgets
# import TKinterModernThemes.examples.layoutdemo as layoutdemo
# import TKinterModernThemes.examples.matplotlibexample as mplexample
#
# def test_every_theme():
#     for mode in ['dark', 'light']:
#         for theme in ['azure', 'forest', 'sun-valley']:
#             print("Running test with mode: ", mode, " and theme: ", theme)
#             allwidgets.App(theme, mode, autorun=False) #autorun loads the modules without running the test
#
# def test_layout_engine(capture_stdout):
#     for mode in ['dark', 'light']:
#         for theme in ['azure', 'forest', 'sun-valley']:
#             print("Running test with mode: ", mode, " and theme: ", theme)
#             capture_stdout['stdout'] = ""
#             layoutdemo.App(theme, mode, autorun=False)
#             assert capture_stdout['stdout'] == open('TKinterModernThemes/examples/layoutdemooutput.txt').read()
#
# def test_matplotlib():
#     for mode in ['dark', 'light']:
#         for theme in ['azure', 'forest', 'sun-valley']:
#             print("Running test with mode: ", mode, " and theme: ", theme)
#             app = mplexample.App(theme, mode, autorun=False)
#             app.addData()
#             app.addData()

def test_load():
    import TKinterModernThemes #forces a basic test of imports
    TKinterModernThemes.firstWindow = False #make sure actually imports