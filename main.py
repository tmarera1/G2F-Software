from multiprocessing import Process, Queue
import thread_serialReader
import thread_visualizerSensor
import nus_central_gui
import rough
# ===============================================================================
# Main
# ===============================================================================
def run():
    try:
        q_force = Queue()
        processes = list([])
        # Start the process for serial connection
        processes = list([
            Process(target=nus_central_gui.main, args=("COM5", q_force,)),
            Process(target=thread_visualizerSensor.plottingThread, args=(q_force, "Force ADC Counts", 800, 35000,)),
            Process(target=rough.CapSense_plot, args = (q_force,)),
        ])
        for p in processes:
            p.start()
    except:
        print("Errors in plotting data")
    finally:
        for p in processes:
            p.join()
        print('Exit the program.')
