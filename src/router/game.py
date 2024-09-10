from fastapi import APIRouter

GAME_PREFIX = "/game"
game_router = APIRouter(prefix=GAME_PREFIX)

GET_GAME = "/{game_id}/get-game/"
START_GAME = "/start-game/"
GET_GAMES = "/get-games/"
CLOSE_GAME = "/{game_id}/close-game/"
UPDATE_GAME = "/{game_id}/update-game/"
CURRENT_QUESTION = "/{game_id}/current-question/"
CHECK_ANSWER = "/{game_id}/check-answer/"
