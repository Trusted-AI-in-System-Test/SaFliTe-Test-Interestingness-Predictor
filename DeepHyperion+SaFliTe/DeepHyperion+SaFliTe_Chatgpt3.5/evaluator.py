
import config

class Evaluator:

    @staticmethod
    def evaluate(ind):
        try:
            ind.test.execute()
            distances = min(ind.test.get_distances())
            ind.test.plot()
            config.EXEC_DONE += 1 
        except Exception as e:
            print("Exception during test execution, skipping the test")
            print(e)
            distances = 10000               
        return distances