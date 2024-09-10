import random

from src.client.database import DBClient
from src.db.game import Game
from src.db.question import Question
from src.db.user import User
from src.schema.game import (
    ActiveGameResponse,
    AnswerRequest,
    AnswerResponse,
    ArchiveGameResponse,
    QuestionResponse,
    UpdateGameRequest,
)
from src.utils.time import get_current_time


class GameService:

    @classmethod
    def parseQuestion(cls, question: Question) -> QuestionResponse:
        return QuestionResponse(
            question_id=question.id,
            question=question.question,
            option_a=question.option_a,
            option_b=question.option_b,
            option_c=question.option_c,
            option_d=question.option_d,
        )

    @classmethod
    def getQuestions(cls, db_client: DBClient) -> Question:
        data: list[Question] = db_client.query(
            Question.get_all,
            error_not_exist=False,
        )
        return random.choice(data)

    @classmethod
    def createGame(cls, user: User, db_client: DBClient) -> ActiveGameResponse:
        question = cls.getQuestions(db_client)
        game = Game(
            user_id=user.id,
            wait_status="1",
            status="active",
            current_questions=[question.id],
        )
        db_client.query(Game.add, items=[game])
        return ActiveGameResponse(
            game_id=game.id,
            current_position="1",
            status="active",
            current_question_progress=0,
            current_question=cls.parseQuestion(question),
        )

    @classmethod
    def getGame(cls, game: Game, db_client: DBClient) -> ActiveGameResponse:
        return ActiveGameResponse(
            game_id=game.id,
            current_position=game.current_position,
            status=game.status,
            current_question_progress=0,
            current_question=cls.getQuestion(game, db_client),
        )

    @classmethod
    def getGames(cls, user: User, db_client: DBClient) -> list[ArchiveGameResponse]:
        games: list[Game] = db_client.query(
            Game.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        return [
            ArchiveGameResponse(
                game_id=game.id,
                created_at=game.created_at,
                status=game.status,
                completed_at=game.completed_at,
            )
            for game in games
        ]

    @classmethod
    def closeGame(cls, game: Game, db_client: DBClient) -> ArchiveGameResponse:
        game.status = "closed"
        game.completed_at = get_current_time()
        db_client.query(Game.update_by_id, id=game.id, new_data=game)
        return ArchiveGameResponse(
            game_id=game.id,
            created_at=game.created_at,
            status=game.status,
            completed_at=game.completed_at,
        )

    @classmethod
    def updateGame(
        cls, game: Game, db_client: DBClient, request: UpdateGameRequest
    ) -> ActiveGameResponse:
        game.current_position = request.current_position
        game.wait_status = request.wait_status
        game.step_percentage += request.point_update
        if game.current_position == "100":
            game.status = "completed"
            game.completed_at = get_current_time()
        db_client.query(Game.update_by_id, id=game.id, new_data=game)
        return ActiveGameResponse(
            game_id=game.id,
            current_position=game.current_position,
            status=game.status,
            current_question_progress=0,
            current_question=cls.getQuestion(game, db_client),
        )

    @classmethod
    def getQuestion(cls, game: Game, db_client: DBClient) -> QuestionResponse:
        question = db_client.query(
            Question.get_id,
            id=game.current_questions[0],
            error_not_exist=False,
        )
        return cls.parseQuestion(question)

    @classmethod
    def checkAnswer(
        cls, game: Game, db_client: DBClient, request: AnswerRequest
    ) -> AnswerResponse:
        question = db_client.query(
            Question.get_id,
            id=request.question_id,
            error_not_exist=False,
        )
        if question.correct_answer_code == request.selected_option:
            question = cls.getQuestions(db_client)
            return AnswerResponse(
                question_id=request.question_id,
                answer_id=game.id,
                status="correct",
                correct_answer_code=question.correct_option,
                next_question=cls.parseQuestion(question),
            )
        return AnswerResponse(
            question_id=request.question_id,
            answer_id=game.id,
            status="incorrect",
            correct_answer_code=question.correct_option,
            next_question=cls.getQuestion(game, db_client),
        )
