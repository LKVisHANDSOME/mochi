from multiprocessing import Process, Pool
import os,time,subprocess
import requests,json
import threading

file_root = "/home/piggy/Final/Dispatch"

def checking_compile_result(Source_id) :
	if os.stat(Source_id).st_size != 0 :
		f = open(Source_id,"r")
		return "CE",f.read()
	else :
		return "AC",""

def check_Runtime_Error(file_place) :
	if os.stat(file_place).st_size != 0 :
		return "RE"
	else :
		return "OK"

def check_TLE_MLE(file_place,Memory_limit) :
	f = open(file_place,"r")
	text = f.readlines()
	res = []
	for i in range(len(text)) :
		res.append(text[i])
	if len(res) == 1 :
		return "OK"
	else :
		memory_size = int(res[1])
		Memory_limit = Memory_limit * 1024
		Maximum = Memory_limit * 0.9
		if memory_size > Maximum :
			return "MLE"
		else :
			return "TLE"

def check_time(file_place) :
	f = open(file_place,"r")
	text = f.readlines()
	res = []
	for i in range(len(text)) :
		res.append(text[i])
	return int((res[1][-5:-2]))+int((res[1][-7:-6]))*1000

def check_memory(file_place) :
	f = open(file_place,"r")
	text = f.readlines()
	return int(text[0])

def check_spec_memory(file_place) :
	f = open(file_place,"r")
	text = f.readlines()
	return int(text[1])


def compare_func(user_file,answer_file) :
	f1 = open(user_file,"r")
	f2 = open(answer_file,"r")

	try : 
		data1 = f1.read()
		data2 = f2.read()

		words1 = data1.split()
		words2 = data2.split()
		f1.close()
		f2.close()
		if words1 != words2 :
			return "WA"
		return "AC"

	except UnicodeError :
		return "OE"


def get_stander_out(file_place) :
	try :
		with open(file_place) as f :
			content = f.read().replace("\n"," ")
			return content
	except UnicodeError :
		return "OE"


def running_func(running_case):
	Mode = int(running_case["Mode"])
	Source_id = running_case["Source_id"]
	Time_limit = running_case["Time_limit"]
	Memory_limit = int(running_case["Memory_limit"])
	Language = running_case["Language"]
	Test_case_name = running_case["Test_case_name"]

	if Mode == 1 :
		Problem_id = running_case["Problem_id"]
		Test_case_answer_name = running_case["Test_case_answer_name"]

		if Language == "c++" or Language == "c" :
			# subprocess.run(["docker run --ulimit cpu=%s --memory %sm -i --rm -v /home/piggy/Final/Dispatch:/home/piggy/Final/Dispatch runner bash -c \" { time /usr/bin/time -f \"%%M\" -o /home/piggy/Final/Dispatch/finish/%s/%s.memory exe/%s </home/piggy/Final/Dispatch/test_case/%s/%s.in 1>/home/piggy/Final/Dispatch/finish/%s/%s.out 2>/home/piggy/Final/Dispatch/finish/%s/%s.err ; } 2>/home/piggy/Final/Dispatch/finish/%s/%s.time \" "%(Time_limit,Memory_limit,Source_id,Test_case_name,Source_id,Problem_id,Test_case_name,Source_id,Test_case_name,Source_id,Test_case_name,Source_id,Test_case_name)],shell=True)
			subprocess.run(["docker run --ulimit cpu=%s --memory %sm -i --rm -v %s:%s runner bash -c \" { time /usr/bin/time -f \"%%M\" -o %s/Submission/%s/%s.memory %s/Submission/%s/%s.exe <%s/Problem/%s/%s.in 1>%s/Submission/%s/%s.out 2>%s/Submission/%s/%s.err ; } 2>%s/Submission/%s/%s.time \" "%(Time_limit,Memory_limit,file_root,file_root,file_root,Source_id,Test_case_name,file_root,Source_id,Source_id,file_root,Problem_id,Test_case_name,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name)],shell=True)


		Runtime_Error_status = check_Runtime_Error("%s/Submission/%s/%s.err"%(file_root,Source_id,Test_case_name))			
		if Runtime_Error_status != "OK" :
			return {"Source_id":Source_id,"Time":-1,"Memory":-1,"Status":Runtime_Error_status,"All_compare_out":{Test_case_name:"RE"}}
		TLE_MLE_status = check_TLE_MLE("%s/Submission/%s/%s.memory"%(file_root,Source_id,Test_case_name),Memory_limit)
		if TLE_MLE_status != "OK" :
			spec_time = check_time("%s/Submission/%s/%s.time"%(file_root,Source_id,Test_case_name))
			spec_memory = check_spec_memory("%s/Submission/%s/%s.memory"%(file_root,Source_id,Test_case_name))
			return {"Source_id":Source_id,"Time":spec_time,"Memory":spec_memory,"Status":TLE_MLE_status,"All_compare_out":{Test_case_name:TLE_MLE_status}}

		Time = check_time("%s/Submission/%s/%s.time"%(file_root,Source_id,Test_case_name))
		Memory = check_memory("%s/Submission/%s/%s.memory"%(file_root,Source_id,Test_case_name))

		if Memory > (Memory_limit*1024) : 
			TLE_MLE_status = "MLE"
			return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":TLE_MLE_status,"All_compare_out":{Test_case_name:TLE_MLE_status}}

		Compare_result = ""
		Compare_result = compare_func("%s/Submission/%s/%s.out"%(file_root,Source_id,Test_case_name),"%s/Problem/%s/%s.ans"%(file_root,Problem_id,Test_case_name))

		return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":Compare_result,"All_compare_out":{Test_case_name:Compare_result}}

	if Mode == 2 :
		Problem_id = running_case["Problem_id"]
		Correct_source_code = running_case["Correct_source_code"]
		if Language == "c++" or Language == "c" :
			subprocess.run(["docker run --ulimit cpu=%s --memory %sm -i --rm -v %s:%s runner bash -c \" { time /usr/bin/time -f \"%%M\" -o %s/Submission/%s/%s.memory %s/Submission/%s/%s.exe <%s/Submission/%s/%s.in 1>%s/Submission/%s/%s.out 2>%s/Submission/%s/%s.err ; } 2>%s/Submission/%s/%s.time \" "%(Time_limit,Memory_limit,file_root,file_root,file_root,Source_id,Test_case_name,file_root,Source_id,Source_id,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name)],shell=True)

		Runtime_Error_status = check_Runtime_Error("%s/Submission/%s/%s.err"%(file_root,Source_id,Test_case_name))			
		if Runtime_Error_status != "OK" :
			return {"Source_id":Source_id,"Time":-1,"Memory":-1,"Status":Runtime_Error_status,"All_compare_out":{Test_case_name:"RE"},"All_stander_out":{Test_case_name:""}}

		Stander_out = get_stander_out("%s/Submission/%s/%s.out"%(file_root,Source_id,Test_case_name))

		if Stander_out == "OE" :
			return {"Source_id":Source_id,"Time":-1,"Memory":-1,"Status":Stander_out,"All_compare_out":{Test_case_name:"OE"},"All_stander_out":{Test_case_name:""}}

		TLE_MLE_status = check_TLE_MLE("%s/Submission/%s/%s.memory"%(file_root,Source_id,Test_case_name),Memory_limit)
		if TLE_MLE_status != "OK" :
			spec_time = check_time("%s/Submission/%s/%s.time"%(file_root,Source_id,Test_case_name))
			spec_memory = check_spec_memory("%s/Submission/%s/%s.memory"%(file_root,Source_id,Test_case_name))
			return {"Source_id":Source_id,"Time":spec_time,"Memory":spec_memory,"Status":TLE_MLE_status,"All_compare_out":{Test_case_name:TLE_MLE_status},"All_stander_out":{Test_case_name:Stander_out}}

		Time = check_time("%s/Submission/%s/%s.time"%(file_root,Source_id,Test_case_name))
		Memory = check_memory("%s/Submission/%s/%s.memory"%(file_root,Source_id,Test_case_name))

		if Memory > (Memory_limit*1024) : 
			TLE_MLE_status = "MLE"
			return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":TLE_MLE_status,"All_compare_out":{Test_case_name:TLE_MLE_status},"All_stander_out":{Test_case_name:Stander_out}}	

		# answer language ???
		subprocess.run(["docker run --ulimit cpu=%s --memory %sm -i --rm -v %s:%s runner bash -c \" { time /usr/bin/time -f \"%%M\" -o %s/Submission/%s/%s.ansmemory %s/Problem/%s/%s.ansexe <%s/Submission/%s/%s.in 1>%s/Submission/%s/%s.ansout 2>%s/Submission/%s/%s.anserr ; } 2>%s/Submission/%s/%s.anstime \" "%(Time_limit,Memory_limit,file_root,file_root,file_root,Source_id,Test_case_name,file_root,Problem_id,Problem_id,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name)],shell=True)

		Runtime_Error_status_answer = check_Runtime_Error("%s/Submission/%s/%s.anserr"%(file_root,Source_id,Test_case_name))			
		if Runtime_Error_status_answer != "OK" :
			return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":"Input Error","All_compare_out":{Test_case_name:"Input Error"},"All_stander_out":{Test_case_name:Stander_out}}

		Stander_out_answer = get_stander_out("%s/Submission/%s/%s.ansout"%(file_root,Source_id,Test_case_name))

		if Stander_out_answer == "OE" :
			return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":"Input Error","All_compare_out":{Test_case_name:"Input Error"},"All_stander_out":{Test_case_name:Stander_out}}

		TLE_MLE_status_answer = check_TLE_MLE("%s/Submission/%s/%s.ansmemory"%(file_root,Source_id,Test_case_name),Memory_limit)
		if TLE_MLE_status_answer != "OK" :
			spec_time_answer = check_time("%s/Submission/%s/%s.anstime"%(file_root,Source_id,Test_case_name))
			spec_memory_answer = check_spec_memory("%s/Submission/%s/%s.ansmemory"%(file_root,Source_id,Test_case_name))
			return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":"Input Error","All_compare_out":{Test_case_name:"Input Error"},"All_stander_out":{Test_case_name:Stander_out}}

		Time_answer = check_time("%s/Submission/%s/%s.anstime"%(file_root,Source_id,Test_case_name))
		Memory_answer = check_memory("%s/Submission/%s/%s.ansmemory"%(file_root,Source_id,Test_case_name))

		if Memory_answer > (Memory_limit*1024) : 
			return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":"Input Error","All_compare_out":{Test_case_name:"Input Error"},"All_stander_out":{Test_case_name:Stander_out}}	


		Compare_result = ""
		Compare_result = compare_func("%s/Submission/%s/%s.out"%(file_root,Source_id,Test_case_name),"%s/Submission/%s/%s.ansout"%(file_root,Source_id,Test_case_name))

		return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":Compare_result,"All_compare_out":{Test_case_name:Compare_result},"All_stander_out":{Test_case_name:Stander_out}}

	if Mode == 3 :

		if Language == "c++" or Language == "c" :
			subprocess.run(["docker run --ulimit cpu=%s --memory %sm -i --rm -v %s:%s runner bash -c \" { time /usr/bin/time -f \"%%M\" -o %s/Submission/%s/%s.memory %s/Submission/%s/%s.exe <%s/Submission/%s/%s.in 1>%s/Submission/%s/%s.out 2>%s/Submission/%s/%s.err ; } 2>%s/Submission/%s/%s.time \" "%(Time_limit,Memory_limit,file_root,file_root,file_root,Source_id,Test_case_name,file_root,Source_id,Source_id,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name,file_root,Source_id,Test_case_name)],shell=True)

		Runtime_Error_status = check_Runtime_Error("%s/Submission/%s/%s.err"%(file_root,Source_id,Test_case_name))			
		if Runtime_Error_status != "OK" :
			return {"Source_id":Source_id,"Time":-1,"Memory":-1,"Status":Runtime_Error_status,"All_compare_out":{Test_case_name:"RE"},"All_stander_out":{Test_case_name:""}}

		Stander_out = get_stander_out("%s/Submission/%s/%s.out"%(file_root,Source_id,Test_case_name))

		if Stander_out == "OE" :
			return {"Source_id":Source_id,"Time":-1,"Memory":-1,"Status":Stander_out,"All_compare_out":{Test_case_name:"OE"},"All_stander_out":{Test_case_name:""}}

		TLE_MLE_status = check_TLE_MLE("%s/Submission/%s/%s.memory"%(file_root,Source_id,Test_case_name),Memory_limit)
		if TLE_MLE_status != "OK" :
			spec_time = check_time("%s/Submission/%s/%s.time"%(file_root,Source_id,Test_case_name))
			spec_memory = check_spec_memory("%s/Submission/%s/%s.memory"%(file_root,Source_id,Test_case_name))
			return {"Source_id":Source_id,"Time":spec_time,"Memory":spec_memory,"Status":TLE_MLE_status,"All_compare_out":{Test_case_name:TLE_MLE_status},"All_stander_out":{Test_case_name:Stander_out}}

		Time = check_time("%s/Submission/%s/%s.time"%(file_root,Source_id,Test_case_name))
		Memory = check_memory("%s/Submission/%s/%s.memory"%(file_root,Source_id,Test_case_name))

		if Memory > (Memory_limit*1024) : 
			TLE_MLE_status = "MLE"
			return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":TLE_MLE_status,"All_compare_out":{Test_case_name:TLE_MLE_status},"All_stander_out":{Test_case_name:Stander_out}}	

		return {"Source_id":Source_id,"Time":Time,"Memory":Memory,"Status":"AC","All_compare_out":{Test_case_name:"AC"},"All_stander_out":{Test_case_name:Stander_out}}	






	# return {"Source_id":Source_id,"Time":"1","Memory":"100","Status":"AC"}

if __name__ == "__main__" :
	requirement = requests.get("http://127.0.0.1:8000")
	req_json = json.loads(requirement.text)

	Submission_count = int(req_json['Submission_Count'])
	result = {"Return_count":Submission_count,"Return_Set":{}}
	running_case = []
	for i in range (0,Submission_count):

		Mode = int(req_json["Submission_Set"][i]["Mode"])

		Problem_id = -1
		if Mode != 3:
			Problem_id = req_json["Submission_Set"][i]["Problem_id"]

		Source_id = req_json["Submission_Set"][i]["Source_id"]

		Test_case_count = int(req_json["Submission_Set"][i]["Test_case_count"])

		Time_limit = req_json["Submission_Set"][i]["Time_limit"]

		Memory_limit = req_json["Submission_Set"][i]["Memory_limit"]

		Language = req_json["Submission_Set"][i]["Language"]

		subprocess.run(["mkdir %s/Submission/%s"%(file_root,Source_id)],shell=True)

		# More Language
		if Language == "c++" :
			subprocess.run(["g++ %s/Submission/%s/%s.cpp -o %s/Submission/%s/%s.exe 2>%s/Submission/%s/%s.compile"%(file_root,Source_id,Source_id,file_place,Source_id,Source_id,file_place,Source_id,Source_id)],shell=True)
		elif Language == "c" :
			subprocess.run(["gcc %s/Submission/%s/%s.c -o %s/Submission/%s/%s.exe 2>%s/Submission/%s/%s.compile"%(file_root,Source_id,Source_id,file_root,Source_id,Source_id,file_root,Source_id,Source_id)],shell=True)

		Status = "AC"
		Compile_error_out=""
		Status , Compile_error_out = checking_compile_result("%s/Submission/%s/%s.compile"%(file_root,Source_id,Source_id))

		result["Return_Set"].update({Source_id:{"Mode":Mode,"Status":Status,"Compile_error_out":Compile_error_out,"Time":"-1","Memory":"-1","All_stander_out":{},"All_compare_out":{}}})

		if Status == "CE" :
			continue

		if Mode == 1 :
			for j in range (0,Test_case_count):
				Test_case_name=req_json["Submission_Set"][i]["All_test_case_general_submission"][j]["Test_case_name"]
				Test_case_answer_name=req_json["Submission_Set"][i]["All_test_case_general_submission"][j]["Test_case_answer_name"]
				running_case.append({"Mode":Mode,"Problem_id":Problem_id,"Source_id":Source_id,"Time_limit":Time_limit,"Memory_limit":Memory_limit,"Language":Language,"Test_case_name":Test_case_name,"Test_case_answer_name":Test_case_answer_name})

		if Mode == 2 :
			Correct_source_code = req_json["Submission_Set"][i]["Correct_source_code"]
			Test_case_name = req_json["Submission_Set"][i]["Self_test_case"][0]["Test_case_name"]
			running_case.append({"Mode":Mode,"Problem_id":Problem_id,"Source_id":Source_id,"Time_limit":Time_limit,"Memory_limit":Memory_limit,"Language":Language,"Correct_source_code":Correct_source_code,"Test_case_name":Test_case_name})
		
		if Mode == 3 :
			for j in range (0,Test_case_count):
				Test_case_name=req_json["Submission_Set"][i]["Self_test_case"][j]["Test_case_name"]
				running_case.append({"Mode":Mode,"Source_id":Source_id,"Time_limit":Time_limit,"Memory_limit":Memory_limit,"Language":Language,"Test_case_name":Test_case_name})


	# threads = []
	# for i in range (0,len(running_case)) :
	# 	threads.append(threading.Thread(target = running_func, args = (running_case[i],)))
	# 	threads[i].start()

	# for i in range (0,len(running_case)) :
	# 	threads[i].join()

	# print("Done")
	pool = Pool()
	running_reslut = pool.map(running_func,running_case)

	for i in range (0,len(running_reslut)) :
		Source_id = running_reslut[i]["Source_id"]
		for key, value in running_reslut[i].items() :
			if key == "Source_id" :
				continue
			if key == "Status" and value != "AC":
				result["Return_Set"][Source_id][key] = value
			elif key == "Time" or key == "Memory" :
				preverious = int(result["Return_Set"][Source_id][key])
				current = int(value)
				result["Return_Set"][Source_id][key] = max(preverious,current)
			elif key == "All_stander_out" :
				result["Return_Set"][Source_id][key].update(value)
			elif key == "All_compare_out" :
				result["Return_Set"][Source_id][key].update(value)

	print(result["Return_Set"])

	# for key,value in result["Return_Set"].items() :
	# 	subprocess.run(["rm -r %s/Submission/%s"%(file_root,key)],shell=True)



	# subprocess.run(["g++ source/main.cpp -o main 1>finish/compile_stdout.log 2>finish/compile_stderr.log"],shell=True)
	# inputs = []
	# for i in range(1,20):
	# 	inputs.append({"test_case":"1.txt","stdout":str(i)+".txt","stderr":str(i)+".txt"})
	# pool=Pool()
	# pool_outputs=pool.map(main_map,inputs)
	# pool.close()
	# pool.join()
	# print(pool_outputs)