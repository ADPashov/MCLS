from threading import Thread

# Snippet how it works if ever needed

# var1 = StringVar()
# t1 = ThreadWithReturn(target=self.model.find_customer, args=[criteria], notify_var=var1)
# t1.start()
# self.view.wait_variable(var1)
# return t1.result


class ThreadWithReturn(Thread):
    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs={}, notify_var=None
    ):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.notify_var = notify_var
        self.result = None

    def run(self):
        self.result = self._target(*self._args, **self._kwargs)
        self.notify_var.set("")
