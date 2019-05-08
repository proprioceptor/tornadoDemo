import tornado.ioloop
import tornado.web
import asyncio
import sqlalchemy as sa
from aiopg.sa import create_engine
from db_setup import create_tables, update_data
from sqlalchemymodels import teachers, studentclasses, students, classes
from tornado.options import define, options

define("debug", default=True, help="run in debug mode")
define("port", default=8888, help="run on the given port", type=int)
define("db_host", default="127.0.0.1", help="tornado database host")
define("db_port", default=5432, help="tornado database port")
define("db_database", default="tornado", help="tornado database name")
define("db_user", default="root", help="tornado database user")
define("db_password", default="root", help="tornado database password")


class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
            (r"/", MainHandler),
            (r"/teacherclasses/([^/]+)/", GetClassesByTeacherHandler),
            (r"/studentclasses/([^/]+)/", GetClassesByStudents),
        ]
        settings = dict(
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hellos, world")


class GetClassesByTeacherHandler(tornado.web.RequestHandler):
    async def get(self, teachers_id):
        async with engine.acquire() as conn:
            async for row in conn.execute(classes.select().where(classes.c.teachers_id == teachers_id)):
                self.write(row.name)


class GetClassesByStudents(tornado.web.RequestHandler):
    async def get(self, student_id):
        async with engine.acquire() as conn:
            join = sa.join(studentclasses, classes, studentclasses.c.classes_id == classes.c.classes_id)
            query = (sa.select([studentclasses, classes], use_labels=True).select_from(join).where(
                studentclasses.c.students_id == student_id))
            async for row in conn.execute(query):
                print(row.classes_name)
                self.write(row.classes_name)
                self.write("\n")


async def create_engines():
    return await create_engine(
        host=options.db_host,
        port=options.db_port,
        user=options.db_user,
        password=options.db_password,
        dbname=options.db_database,
    )


async def main():
    tornado.options.parse_command_line()

    async with create_engine(
            host=options.db_host,
            port=options.db_port,
            user=options.db_user,
            password=options.db_password,
            dbname=options.db_database
    ) as db:
        async with db.acquire() as conn:
            await create_tables(conn)
        async with db.acquire() as conn:
            await update_data(conn)
        app = Application(db)
        app.listen(options.port)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(main())
        engine = loop.run_until_complete(create_engines())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()
