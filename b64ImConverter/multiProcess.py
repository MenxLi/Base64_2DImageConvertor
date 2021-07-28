import typing, math, os
import multiprocessing, tempfile, pickle

def divideChunks(lis: typing.Iterable, n_size: int) -> typing.Iterator:
    for i in range(0, len(lis), n_size): 
        yield lis[i:i + n_size]

def inferWorkers() -> int:
	workers = multiprocessing.cpu_count() - 1
	return workers

def lisJobParallel(func: typing.Callable, list_like: typing.Iterable, use_buffer:bool = False, n_workers: int = -1) -> list:
	"""
	parallel a job that is applied to a list-like object
	The paralleled function should only take one argument which is the list_like
	the function should be able to be run on subset of the list_like
	and return list-like results or None
	i.e. 
		func(list_like) -> list_like2 | None
	- list_like: list-like argument
	- n_workers: number of process, set to -1 for using auto-inferring
	- use_buffer: use hard disk as buffer for each subprocess output, enable when the data exchange is large
	"""
	if n_workers <= 0:
		n_workers = inferWorkers()

	data = list_like
	chunk_size = math.ceil(len(data)/n_workers)
	conns = []
	procs = []

	# define the function for multiprocessing.Process
	def processFunc(conn, func_, data_):
		out_ = func_(data_)
		if use_buffer:
			f_path = tempfile.NamedTemporaryFile(mode = "w+b").name
			with open(f_path, "wb") as fp:
				bytes = pickle.dumps(out_)
				fp.write(bytes)
			conn.send(f_path)
		else:
			conn.send(out_)

	# Create and run the processes	
	for d in divideChunks(data, chunk_size):
		conn1, conn2 = multiprocessing.Pipe()
		process = multiprocessing.Process(\
			target=processFunc, args=(conn1, func, d))
		conns.append(conn2)
		procs.append(process)
		process.start()
	for p in procs:
		p.join()
	
	# Concatenate results
	out = []
	for conn_ in conns:
		obj = conn_.recv()
		if use_buffer:
			with open(obj, "rb") as fp:
				out_ = pickle.loads(fp.read())
			os.remove(obj)	# delete the temporary buffer file
		else:
			out_ = obj
		# concatenate
		if out_ is not None:
			out = [*out, *out_]
		else:
			out.append(None)
	return out
