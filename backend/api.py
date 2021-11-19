from flask_restful import Api, Resource, reqparse
import datetime

problem_post_args = reqparse.RequestParser()
problem_post_args.add_argument("name",type=str,required=True,help='name is required!')
problem_post_args.add_argument("questioner_id",type=int,required=True,help='questioner_id is required!')
problem_post_args.add_argument("difficulty",type=int,required=True,help='difficulty is required!')
problem_post_args.add_argument("content",type=str,required=True,help='content is required!')
problem_post_args.add_argument("time_limit",type=int,required=True,help='time_limit is required!')
problem_post_args.add_argument("memory_limit",type=int,required=True,help='memory_limit is required!')
problem_post_args.add_argument("testcase_count",type=int,required=True,help='testcase_count is required!')
problem_post_args.add_argument("sample_input",type=str,required=True,help='sample_input is required!')
problem_post_args.add_argument("is_hidden",type=int,required=True,help='is_hidden is required!')

# problem_get_args = reqparse.RequestParser()
# problem_get_args.add_argument("page",type=int,required=True,help='page is required!')



class problem(Resource):
    def get(self,page,name,difficulty,topic):
        return {"string":"Hello_world","name":name,"page":page,"difficulty":difficulty}

    def post(self):
        problem = problem_post_args.parse_args()
        from models import Problem
        new_problem = Problem(questioner_id=problem.questioner_id,name=problem.name,difficulty=problem.difficulty,
        content=problem.content,time_limit=problem.time_limit,memory_limit=problem.memory_limit,testcase_count=problem.testcase_count,
        sample_input=problem.sample_input,is_hidden=problem.is_hidden,upload_date = datetime.datetime.now()+datetime.timedelta(hours = 8))
        from app import db
        db.session.add(new_problem)
        db.session.commit()
        return 200



