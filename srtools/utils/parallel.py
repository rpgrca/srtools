"""Threading utilities."""
from Queue import Queue
from threading import Thread
#import logging
from srtools.utils.loggingutils import log_debug

#LOGGER = logging.getLogger(__name__)

class Worker(Thread):
    """No documentation"""
    def __init__(self, thread_id, tasks, results):
        super(Worker, self).__init__()

        self.thread_id = thread_id
        self.tasks = tasks
        self.results = results
        self.daemon = True

    def run(self):
        log_debug('Worker %s launched', self.thread_id)
        while True:
            task_id, func, args, kwargs = self.tasks.get()
            log_debug('Worker %s start to work on %s', self.thread_id, func.__name__)
            try:
                self.results.put_nowait((task_id, func(*args, **kwargs)))
            except BaseException as err:
                log_debug('Thread(%s): error with task %s\n%s',
                          self.thread_id, repr(func.__name__), err)
            finally:
                log_debug('Worker %s finished work on %s', self.thread_id, func.__name__)
                self.tasks.task_done()

class Parallel(object):
    """Handles parallel execution."""
    def __init__(self, thread_num=10):
        # create queues
        self.tasks_queue = Queue()
        self.results_queue = Queue()

        # create a threading pool
        self.pool = []
        for i in range(thread_num):
            worker = Worker(i, self.tasks_queue, self.results_queue)
            self.pool.append(worker)
            worker.start()

        log_debug('Created %s workers', thread_num)

    def add_task(self, task_id, func, *args, **kwargs):
        """
        Add task to queue, they will be started as soon as added
        :param func: function to execute
        :param args: args to transmit
        :param kwargs: kwargs to transmit
        """

        log_debug('Adding one task to queue (%s)', func.__name__)
        # add task to queue
        self.tasks_queue.put_nowait((task_id, func, args, kwargs))

    def get_results(self):
        """No documentation."""
        log_debug('Waiting for processes to ends')
        self.tasks_queue.join()
        log_debug('Processes terminated, fetching results')

        results = []
        while not self.results_queue.empty():
            results.append(self.results_queue.get())

        log_debug('Results fetched, returning data')
        return dict(results)
