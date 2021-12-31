from flask import json, jsonify, url_for, redirect, flash, render_template, request
from flask_login.utils import login_required
from flask_restful import Api, Resource, abort
from flask_mail import Message
import datetime
from backend.exception import *
from backend.models import *
from backend import bcrypt, app, mail, BASE
from backend.argument import *
#from backend.argument import signup_post_args, submission_post_args, login_post_args, user_profile_put_args, problem_post_args, problem_put_args, problem_get_args, queue_post_args, dispatcher_post_args
# 8同理9
from flask_login import login_user, current_user, logout_user, login_required
import os


class lazy(Resource):
    def get(self):
        from backend.convert_file_to_json import convert_file_to_testcase
        return convert_file_to_testcase()

    def post(self):
        if 'lan' in request.args:
            lan = request.args['lan']
        else:
            return "Error, lan is required"
        from backend.convert_file_to_json import convert_file_to_code
        return convert_file_to_code(lan)


class check(Resource):
    def get(self):
        queues = Queue.query.all()
        res = {}
        res["returnSet"] = []
        for q in queues:
            res["returnSet"].append(q.as_dict())
        return res


class delete_dir(Resource):
    def delete(self):
        import shutil
        shutil.rmtree(BASE+'buffer')
        os.mkdir(BASE+'buffer')
        if os.path.isdir(BASE+"Problem"):
            shutil.rmtree(BASE+'Problem')
            os.mkdir(BASE+'Problem')
        return "delete success"


class reset_database(Resource):
    def delete(self):
        from backend import db
        db.drop_all()
        db.create_all()
        db.session.commit()
        return "delete success"


class problem(Resource):
    def get(self):
        if 'page' in request.args:
            page = request.args['page']
        else:
            return "Error, page is required"
        topic = None
        difficulty = None
        name = None
        if 'topic' in request.args:
            topic = request.args['topic']
        if 'difficulty' in request.args:
            difficulty = request.args['difficulty']
        if 'name' in request.args:
            name = request.args['name']

        problems = Problem.query.all()
        ''' if topic and difficulty and name:
            from backend import db
            problems = Problem.query.filter(db.and_(db.and_(Problem.topic==topic,Problem.difficulty==difficulty),Problem.name.like(name))).all()
        elif topic:
            problems = Problem.query.filter(Problem.topic==topic).all()
        elif topic and difficulty:
            problems = Problem.query.filter(db.and_(Problem.difficulty==difficulty,Problem.topic==topic)).all()'''

        if difficulty and name:
            from backend import db
            problems = Problem.query.filter(
                db.and_(Problem.difficulty == difficulty, Problem.name.like(name))).all()
        elif difficulty:
            problems = Problem.query.filter(
                Problem.difficulty == difficulty).all()
        elif name:
            problems = Problem.query.filter(Problem.name.like(name)).all()

        if problems:
            ret = {}
            ret["returnset"] = []
            for problem in problems:
                ret["returnset"].append({
                    "id": problem.problem_id,
                    "name": problem.name,
                    "difficulty": problem.difficulty
                })
            return jsonify(ret)
        return "don't have any problem", 404

    def post(self):
        problem = problem_post_args.parse_args()
        if_problemname_has_existed(problem.name)
        now = Queue.query.filter_by(source_id=problem.source_id).first()
        new_problem = Problem(questioner_id=problem.questioner_id, name=problem.name, difficulty=problem.difficulty, content=problem.content, time_limit=problem.time_limit, memory_limit=problem.memory_limit,
                              testcase_count=now.test_case_count, sample_input=problem.sample_input, is_hidden=problem.is_hidden, upload_date=datetime.datetime.now(), correct_source_code=problem.correct_source_code, correct_answer_language=problem.correct_answer_language)

        if now.status == 0:
            return "not ok"
        if not os.path.isdir(BASE+"buffer"):
            os.mkdir(BASE+"buffer")
        path = BASE+"buffer/"+str(now.user_id)
        import shutil
        if not os.path.isdir(BASE+"Problem"):
            os.mkdir(BASE+"Problem")
        # os.rename(BASE+"buffer/"+str(now.user_id)+'/'+str(now.source_id)+'.ansexe',
                #   BASE+"buffer/"+str(now.user_id)+'/'+str(Problem.query.count()+1)+'.ansexe')
        shutil.move(path, BASE+"Problem/"+str(Problem.query.count()+1))
        from backend import db
        for i in range(now.test_case_count):
            test_case = Problem_Testcase(problem_id=Problem.query.count(
            )+1, testcase_id=i+1, input_name=str(i+1)+'.in', output_name=str(i+1)+'.ans')
            db.session.add(test_case)
        db.session.add(new_problem)
        db.session.delete(now)
        db.session.commit()
        return "Success to add problem", 200


class create_problem_test_run(Resource):
    def get(self):
        if 'source_id' in request.args:
            source_id = request.args['source_id']
        else:
            return "Error, source_id is required"

        if 'user_id' in request.args:
            user_id = request.args['user_id']
        else:
            return "Error, user_id is required"
        now = Queue.query.filter_by(source_id=source_id).first()
        if now.status == 0:
            return "not ok"
        if not os.path.isdir(BASE+"buffer"):
            os.mkdir(BASE+"buffer")
        path = BASE+"buffer/"+str(user_id)
        res = {}
        res["test_case_count"] = now.test_case_count
        res["return_set"] = []
        for i in range(now.test_case_count):
            with open(path+"/"+str(i+1)+'.ans', mode="r", encoding="utf-8") as file:
                temp = file.read()
                res["return_set"].append(temp)

        return res

    def post(self):
        args = create_problem_test_run_args.parse_args()
        if not os.path.isdir(BASE+"buffer"):
            os.mkdir(BASE+"buffer")
        path = BASE+"buffer/"+str(args.user_id)
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            return "Error, XD"
        input_set = args["test_case"]
        new_queue = Queue(user_id=args.user_id, mode=3, language=args.language, test_case_count=len(input_set), upload_date=str(
            datetime.datetime.now()), code_content=args.code_content)
        from backend import db
        db.session.add(new_queue)
        db.session.commit()

        # omgomg
        with open(path+"/"+"correct_source_code"+'.'+str(args.language), mode="w", encoding="utf-8") as file:
            file.write(args.code_content)
        cnt = 1
        for testcase in input_set:
            with open(path+'/'+str(cnt)+".in", mode='w', encoding="utf-8") as file:
                file.write(testcase)
            cnt += 1

        return 200, new_queue.source_id


class test_run(Resource):
    def get(self):
        if 'source_id' in request.args:
            source_id = request.args['source_id']
        else:
            return "Error, source_id is required"
        if 'user_id' in request.args:
            user_id = request.args['user_id']
        else:
            return "Error, user_id is required"
        now = Queue.query.filter_by(source_id=source_id).first()
        if now.status == 0:
            return "not ok"
        # from backend.convert_file_to_json import convert_file_to_json as yea
        # res = yea("buffer/"+str(source_id)+'.ans')
        if not os.path.isdir(BASE+"buffer"):
            os.mkdir(BASE+"buffer")
        with open(BASE+"buffer/"+str(source_id)+".ans", mode="r", encoding="utf-8") as file:
            res = file.read()
        from backend import db
        db.session.delete(now)
        db.session.commit()
        return res

    def post(self):
        from backend import db
        args = test_run_post_args.parse_args()
        if not os.path.isdir(BASE+"buffer"):
            os.mkdir(BASE+"buffer")
        new_queue = Queue(user_id=args.user_id, mode=2, problem_id=args.problem_id, language=args.language, upload_date=str(
            datetime.datetime.now()), code_content=args.code_content, test_case_count=1)
        source_id = Queue.query.count()+1
        with open(BASE+"buffer/"+str(source_id)+".in", mode="w", encoding="utf-8") as file:
            file.write(args.test_case)
        with open(BASE+"buffer/"+str(source_id)+'.'+str(args.language), mode="w", encoding="utf-8") as file:
            file.write(args.code_content)
        db.session.add(new_queue)
        db.session.commit()
        return 200, source_id


class problem_id(Resource):
    def get(self, problem_id):
        problem = Problem.query.filter_by(problem_id=problem_id).first()
        return problem.as_dict()

    #!!
    def put(self, problem_id):
        args = problem_put_args.parse_args()
        problem = Problem.query.filter_by(problem_id=problem_id).first()
        if problem == None:
            return "problem_id does not exist", 500
        if args.name:
            if_problemname_has_existed(args.name, problem_id)
            problem.name = args.name
        if args.difficulty:
            problem.difficulty = args.difficulty
        if args.content:
            problem.content = args.content
        if args.time_limit:
            problem.time_limit = args.time_limit
        if args.memory_limit:
            problem.memory_limit = args.memory_limit
        if args.sample_input:
            problem.sample_input = args.sample_input
        if args.testcase_count:
            problem.testcase_count = args.testcase_count
        if args.is_hidden:
            problem.is_hidden = args.is_hidden
        if args.correct_source_code:
            problem.correct_source_code = args.correct_source_code

        from backend import db
        db.session.commit()
        return "Success to put problem", 200

    #!!
    def delete(self, problem_id):
        problem = Problem.query.filter_by(problem_id=problem_id).delete()
        from backend import db
        db.session.commit()
        return "Success to delete problem", 200


class problem_solution(Resource):
    def get(self, problem_id):
        problem = Problem.query.filter_by(problem_id=problem_id)
        if problem == None:
            return "problem does not exist", 404

        return problem.correct_source_code


class problem_submission(Resource):
    def get(self, problem_id, user_id=-1):
        problem = Problem.query.filter_by(problem_id=problem_id)
        if problem == None:
            return "problem does not exist", 400
        user = User.query.filter_by(user_id=user_id)
        if user == None:
            return "user does not exist", 400
        if user_id != -1:
            submissions = Submission.query.filter_by(
                **{"user_id": user_id, "problem_id": problem.problem_id}).all()
        else:
            submissions = Submission.query.filter_by(
                problem_id=problem.problem_id).all()

        if submissions:
            ret = {}
            ret["returnset"] = []
            for submission in submissions:
                ret["returnset"].append({
                    "submission_id": submission.submission_id,
                    "problem_id": problem.problem_id,
                    "name": user.name,
                    "status": submission.status,
                    "language": submission.language,
                    "upload_date": submission.upload_date
                })
            return jsonify(ret)
        return "you have not tried this problem"


class status(Resource):
    def get(self):
        if 'page' in request.args:
            page = request.args['page']
        else:
            return jsonify("message : Error, page is required")

        submissions = Submission.query.all()
        ret = {}
        ret["returnset"] = []
        for submission in submissions:
            ret["returnset"].append({
                "submission_id": submission.submission_id,
                "problem_id": problem.problem_id,
                "name": User.name,
                "status": submission.status,
                "language": submission.language,
                "upload_date": submission.upload_date
            })
        return jsonify(ret)


class signup(Resource):
    def post(self):
        if current_user.is_authenticated:
            return jsonify("message : Had logged in")
        args = signup_post_args.parse_args()
        if_username_has_existed(args.name)
        is_email_format(args.email)
        if_email_has_existed(args.email)
        confirm_password_equal_password(args.password, args.confirm_password)
        hashed_password = bcrypt.generate_password_hash(
            args.password).decode('utf-8')
        new_user = User(name=args.name, email=args.email,
                        password=hashed_password, register_date=datetime.datetime.now())
        from backend import db
        db.session.add(new_user)
        db.session.commit()
        return jsonify("message : success to login")


class login(Resource):
    def get(self):
        return render_template('login.html')

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        args = login_post_args.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if user and bcrypt.check_password_hash(user.password, args.password):
            login_user(user, remember=args.remember)
            return jsonify("message : Success to login.")
        elif user:
            return jsonify("message : wrong password")
        else:
            abort(404, message="Couldn't find the user")


class reset_sent_email(Resource):
    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        args = request_reset_post_args.parse_args()
        reset_check_email(args.email)
        user = User.query.filter_by(email=args.email).first()
        token = user.get_reset_token()
        recipient = args.email
        title = "Reset your password."
        msg = Message(title, recipients=[recipient])
        msg.body = token
        mail.send(msg)
        return


class reset_password(Resource):
    def put(self, token):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        user = User.verify_reset_token(token)
        if user is None:
            flash('This is an invalid or expired token', 'warning')
            return "Invalid"
        args = reset_password_put_args.parse_args()
        confirm_password_equal_password(args.password, args.confirm_password)
        hashed_password = bcrypt.generate_password_hash(
            args.password).decode('utf-8')
        user.password = hashed_password
        from backend import db
        db.session.commit()


class logout(Resource):
    def logout():
        logout_user()
        return redirect(url_for('home'))

# if no login 401


class user_profile(Resource):
    @login_required
    def get(self, user_id):
        from backend import db
        user = User.query.filter_by(id=user_id).first_or_404()
        ACs = User_problem.query.filter_by(user_id=user.id, status=1).all()
        datas = []
        for AC in ACs:
            datas.append(AC.problem_id)
        return jsonify({"name": user.name, "email": user.email, "register_date": str(user.register_date), "user_problem": datas})

    def put(self):
        args = user_profile_put_args.parse_args()
        if_username_has_existed(args.name)
        if_email_has_existed(args.email)
        self = args
        from backend import db
        db.session.commit()


class submission_data(Resource):
    def get(self, submission_id):
        from backend import db
        submission = Submission.query.filter_by(
            submission_id=submission_id).first_or_404()
        return submission.as_dict()


class queue_new(Resource):
    def post(self):
        from backend import db
        args = queue_post_args.parse_args()
        problem = Problem.query.filter_by(problem_id=args.problem_id).first()
        new_queue = Queue(user_id=args.user_id, problem_id=args.problem_id, mode=1, exam_id=args.exam_id,
                          homework_id=args.homework_id, language=args.language, upload_date=str(datetime.datetime.now()), code_content=args.code_content, test_case_count=problem.testcase_count)

        if not os.path.isdir(BASE+"buffer/"):
            os.mkdir(BASE+"buffer/")

        with open(BASE+"buffer/"+str(Queue.query.count() + 1)+'.'+str(args.language), mode="w", encoding="utf-8") as file:
            file.write(args.code_content)

        db.session.add(new_queue)
        db.session.commit()
        return 200


class dispatcher(Resource):
    def get(self):
        from backend import db
        from backend.convert_file_to_json import convert_file_to_json as yea
        queues = Queue.query.limit(20).all()
        datas = {}
        datas["Submission_Set"] = []
        cnt = 0
        for queue in queues:
            if queue.status == 1:
                continue
            if cnt > 10:
                break
            data = {}
            data["Mode"] = queue.mode
            if queue.mode in [1, 2]:
                data["Problem_id"] = queue.problem_id
            data["User_id"] = queue.user_id
            data["Source_id"] = queue.source_id
            data["Keep"] = 0
            problem = Problem.query.filter_by(
                problem_id=queue.problem_id).first()
            if problem == None and queue.mode in [1, 2]:
                return "no problem's id = " + str(queue.problem_id)
            data["Test_case_count"] = queue.test_case_count
            if queue.mode in [1, 2]:
                data["Time_limit"] = problem.time_limit
                data["Memory_limit"] = problem.memory_limit
            else:
                data["Time_limit"] = queue.time_limit
                data["Memory_limit"] = queue.memory_limit
            data["Language"] = queue.language
            if queue.mode in [1, 2]:
                data["Correct_answer_language"] = problem.correct_answer_language
            if queue.mode in [1, 2]:
                data["Correct_source_code"] = problem.correct_source_code
            if queue.mode in [1, 2]:
                data["Code"] = yea(
                    "buffer/"+str(queue.source_id)+'.'+str(queue.language))
            else:
                data["Code"] = yea(
                    "buffer/"+str(queue.user_id)+"/correct_source_code"+'.'+str(queue.language))
            data["All_test_case_general_submission"] = []
            data["Self_test_case"] = []
            if queue.mode == 1:
                testcases = Problem_Testcase.query.filter_by(
                    problem_id=queue.problem_id).all()
                for i in range(len(testcases)):
                    data["All_test_case_general_submission"].append(
                        {"Test_case_name": testcases[i].input_name.replace('.in', ""), "Test_case_answer_name": testcases[i].output_name.replace('.ans', "")})

            if queue.mode == 2:
                data["Self_test_case"].append(
                    {"Test_case_name": str(queue.source_id),
                     "Data": yea(
                        "buffer/"+str(queue.source_id)+'.in')
                     })
            if queue.mode == 3:
                for i in range(queue.test_case_count):
                    data["Self_test_case"].append(
                        {"Test_case_name": str(i+1),
                         "Data": yea(
                            "buffer/"+str(queue.user_id)+"/"+str(i+1)+'.in')
                         })

            datas["Submission_Set"].append(data)
            cnt += 1

        datas["Submission_Count"] = cnt
        return jsonify(datas)

    def post(self):
        from backend import db
        args = dispatcher_post_args.parse_args()
        count = args["Return_count"]
        for submission in args["Return_Set"]:
            data = Queue.query.filter_by(
                source_id=submission["Source_id"]).first()
            if data == None:
                queues = Queue.query.all()
                res = {}
                res["returnSet"] = []
                res["disappeared_source_id"] = submission["Source_id"]
                for q in queues:
                    res["returnSet"].append(q.as_dict())
                print(res)
                continue
            if data.mode == 1:
                if data.exam_id:
                    status=submission["Status"]
                    upload_date=data.upload_date
                    exam = Exam.query.filter_by(exam_id=exam_id).first()
                    dashboard = dashboard.query.filter_by(exam_id=data.exam_id,user_id=data.user_id).first()
                    dash = Dashboard_with_problem.query.filter_by(exam_id=data.exam_id,user_id=data.user_id,problem_id=data.problem_id).first()
                    from backend import db
                    if dashboard == None:
                        dashboard = Dashboard(exam_id=data.exam_id,user_id=data.user_id,solved_count=0,total_time=0)
                        db.session.add(dashboard)
                    if dash == None:
                        problem = Exam_problem.query.filter_by(exam_id=data.exam_id,problem_id=problem_id).first()
                        if status == 0:
                            dash = Dashboard_with_problem(exam_id=data.exam_id,user_id=data.user_id,problem_id=data.problem_id,sequence=problem.sequence,try_count=1,current_status=0)
                        else:
                            dash = Dashboard_with_problem(exam_id=data.exam_id,user_id=data.user_id,problem_id=data.problem_id,sequence=problem.sequence,try_count=1,solved_time=upload_time - exam.start_time,current_status=0)
                            dashboard.solved_count += 1
                            dashboard.total_time += dash.solved_time
                        db.session.add(dash)
                    else:
                        dash.try_count+=1
                        if status == 1:
                            if dash.current_status == 0: 
                                dash.current_status = 1
                                dash.solved_time = upload_time - exam.start_time
                                dashboard.solved_count+=1
                                dashboard.total_time += dash.solved_time + (dash.try_count - 1) * 20
                    db.session.commit()

                        
                elif data.homework_id:
                    XD
                new_submission = Submission(user_id=data.user_id, problem_id=data.problem_id, source_id=submission["Source_id"], status=submission["Status"], code_content=data.code_content, exam_id=data.exam_id, homework_id=data.homework_id, error_hint=submission[
                    "Compile_error_out"], error_line=0, language=data.language, time_used=submission["Time"], memory_used=submission["Memory"], upload_date=data.upload_date)
                db.session.add(new_submission)
                Queue.query.filter_by(
                    source_id=submission["Source_id"]).delete()
            elif data.mode == 2:
                data.status = 1
                if not os.path.isdir(BASE+"buffer/"):
                    os.mkdir(BASE+"buffer/")
                with open(BASE+"buffer/"+str(data.source_id)+".ans", mode="w", encoding="utf-8") as file:
                    file.write(submission["All_stander_out"]
                               [str(data.source_id)])
            else:
                data.status = 1
                if not os.path.isdir(BASE+"buffer/"+str(data.user_id)+"/"):
                    os.mkdir(BASE+"buffer/"+str(data.user_id)+"/")
                cnt = 1
                for i in range(len(submission["All_stander_out"])):
                    with open(BASE+"buffer/"+str(data.user_id)+"/"+str(cnt)+".ans", mode="w", encoding="utf-8") as file:
                        file.write(submission["All_stander_out"][str(i+1)])
                    cnt += 1
        db.session.commit()
        return "success to return", 200


class class_all(Resource):
    def get(self):  #給所有班級資訊
        if 'page' in request.args:
            page = request.args['page']
        else:
            return "Error, page is required"

        classes = Class.query.all()
        if classes:
            ret = {}
            ret["returnset"] = []
            for a_class in classes:
                user = User.query.filter_by(user_id=a_class.teacher_id).first()
                ret["returnset"].append({
                    "id": a_class.id,
                    "name": a_class.name,
                    "semester": a_class.semester,
                    "teacher_name": user.name,
                    "public": is_public
                })
            return jsonify(ret)
        return "don't have any class", 404

    def post(self):    #新增班級，需要teacher的user_id,class_name,semester,is_public
        if 'user_id' in request.args:
            teacher_id = request.args['user_id']
        else:
            return "Error, user_id is required"

        if 'class_name' in request.args:
            class_name = request.args['class_name']
        else:
            return "Error, class_name is required"

        if 'semester' in request.args:
            semester = request.args['semester']
        else:
            return "Error, semester is required"

        if 'is_public' in request.args:
            is_public = request.args['is_public']
        else:
            return "Error, is_public is required"

        import random
        import string
        while 1:
            s = ''.join(random.choice(string.ascii_letters + string.digits)for x in range(10))
            search = Class.filter_by(invite_code=s).first()
            if search == None:
                break

        user = User.query.filtyer_by(user_id=teacher_id)
        new_class = Class(name=a_class.name, semester=a_class.semester, teacher_name=user.name,
                          public=is_public, invite_code=s,teacher_id=teacher_id)
        new_user_class = User_class(class_id=Class.query.count()+1,user_id=teacher_id,student_id=-1,authority=1)
        from backend import db
        db.session.add(new_class)
        db.session.commit()
        return "success, invite code = " + s , 200


class A_class(Resource):
    def get(self,class_id):
        a_class = Class.query.filter_by(class_id=class_id).first()
        if a_class == None:
            return "class is not found", 404
        user = User.query.filter_by(user_id=a_class.teacher_id).first()
        ret = {
            "id": a_class.id,
            "name": a_class.name,
            "semester": a_class.semester,
            "teacher_name": user.name,
            "is_public": a_class.public,
            "invite_code": a_calss.invite_code
        }
        return jsonify(ret)
            

    def put(): # 更新教室相關資訊
        XD

class class_member(Resource):
    def get(self,class_id): #get教室成員
        a_class = Class_user.query.filter_by(class_id=class_id).all()
        if a_class == None:
            return "class is not found",404
        if a_class:
            ret = {}
            ret["returnset"] = []
            for student in a_class:
                user = User.query.filter_by(user_id=student.user_id)
                ret["returnset"].append({
                    "id": user.id,
                    "name": user.name
                })
            return jsonify(ret)
        return jsonify({})

class add_member_to_class(Resource):
    def get(self):    #確認邀請碼是否正確
        if 'class_id' in request.args:
            class_id = request.args['class_id']
        else:
            return "Error, class_id is required"
        
        if 'invite_code' in request.args:
            invite_code = request.args['invite_code']
        else:
            return "Error, invite_code is required"

        the_class = Class.query.filter_by(class_id=class_id).first()
        if the_class == None:
            return "class is not found",404
        if the_class.invite_code != invite_code:
            return "invite code is wrong"
        return "invite code is correct",200

    def put(self):  #新增同學到教室，給我user_id和student_id(學號)更新table
        if 'class_id' in request.args:
            class_id = request.args['class_id']
        else:
            return "Error, class_id is required"
        
        if 'user_id' in request.args:
            user_id = request.args['user_id']
        else:
            return "Error, user_id is required"

        if 'student_id' in request.args:
            student_id = request.args['student_id']
        else:
            return "Error, student_id is required"


        the_class = Class.query.filter_by(class_id=class_id).first()
        if the_class == None:
            return "class is not found",404
        if the_class.invite_code != invite_code:
            return "invite code is wrong"
        
        new_user_class = User_class(class_id=class_id,user_id=user_id,student_id=student_id,authority=0)
        from backend import db
        db.session.add(new_user_class)
        db.session.commit()
        return "add member success",200



class exam(Resource):
    def get(self): #確認使用者有沒有權限
        if 'class_id' in request.args:
            class_id = request.args['class_id']
        else:
            return "Error, class_id is required"
        
        if 'user_id' in request.args:
            user_id = request.args['user_id']
        else:
            return "Error, user_id is required"
        exam_class = Class.query.filter_by(class_id=class_id).first()
        if exam_class.teacher_id != user_id:
            return "only teacher can create exam",403
        return "OK",200

    def post(self): #新增考試
        if 'class_id' in request.args:
            class_id = request.args['class_id']
        else:
            return "Error, class_id is required"
        
        if 'user_id' in request.args:
            user_id = request.args['user_id']
        else:
            return "Error, user_id is required"

        if 'exam_name' in request.args:
            exam_name = request.args['exam_name']
        else:
            return "Error, exam_name is required"

        if 'exam_info' in request.args:
            exam_info = request.args['exam_info']
        else:
            return "Error, exam_info is required"

        if 'exam_start_time' in request.args:
            exam_start_time = request.args['exam_start_time']
        else:
            return "Error, exam_name is required"

        if 'exam_end_time' in request.args:
            exam_end_time = request.args['exam_end_time']
        else:
            return "Error, exam_end_time is required"
        
        if 'problem_set' in requerst.args:
            problem_set = request.args['problem_set']
        else:
            return "Error, problem_set is required"

        exam = Exam(class_id=class_id,name=exam_name,start_time=exam_start_time,end_time=exam_end_time,exam_info=exam_info)
        from backend import db
        
        cnt = 1
        for a_problem in problemset:
            new_exam_problem = Exam_problem(exam_id=Exam.query.count()+1,problem_id=a_problem,sequence=cnt)
            cnt+=1
            db.session.add(new_exam_problem)
            
        db.session.add(exam)
        db.session.commit()
        return "success to add exam",300


class dashboard(Resource):
    def get(self,exam_id):  #回傳dashboard table
        lines = Dashboard.query.filter_by(exam_id=exam_id).all()
        if lines == None:
            return "Error, dashboard hadn't been created",404
        problem_set = []
        exam_problems = Exam_problem.filter_by(exam_id=exam_id).all()
        for exam_problem in exam_problems:
            problem_set.append(exam_problem.problem_id)
        ret = {}
        ret["return_set"]=[]
        for line in lines:
            user = User.query.filter_by(user_id=line.user_id).first()
            a_student={}
            a_student["name"] = user.name
            a_student["solved"] = line.solved_count
            dashs = Dashboard_with_problem.query.filter_by(user_id=line.user_id).all()
            a_student["problem_status"]=[]
            a_student["problem_time"]=[]
            a_student["problem_try_count"]=[]
            for dash in dashs:
                a_student["problem_status"].append(dash.current_status)
                a_student["problem_time"].append(dash.solved_time)
                a_student["problem_try_count"].append(dash.try_count)
            ret["return_set"].append(a_student)
        return ret

    def post(self): #初始化dashboard table
        if 'exam_id' in request.args:
            exam_id = request.args['exam_id']
        else:
            return "Error, exam_id is required"
        exam = Exam.query.filter_by(exam_id=exam_id).first()
        problem_set = Exam_problem.query.filter_by(exam_id=exam_id).all()
        class_id = exam.class_id
        students = Class_user.query.filter_by(class_id=class_id).all()
        from backend import db
        for student in students:
            new_dashboard = Dashboard(exam_id=exam_id,user_id=student.user_id)
            db.session.add(new_dashboard)
            for problem in problem_set:
                dash = Dashboard_with_problem(exam_id=exam_id,user_id=student.user_id,problem_id=problem.problem_id,sequence=problem.sequence,try_count=0,solved_time=-1,current_status=-1)
                db.session.add(dash)
        db.session.commit()
        return "create_succes",200
