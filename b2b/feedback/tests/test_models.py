import pytest
from django.contrib.auth import get_user_model
from feedback.models import (
    Answer,
    AnswerChoice,
    Client,
    Question,
    QuestionChoice,
    Questionnaire,
    Response,
)
from model_bakery import baker

User = get_user_model()


@pytest.mark.django_db
class TestModels:
    def test_client_creation(self):
        client = baker.make(Client)
        assert isinstance(client, Client)
        assert str(client) == client.name

    def test_questionnaire_creation(self):
        questionnaire = baker.make(Questionnaire)
        assert isinstance(questionnaire, Questionnaire)
        assert str(questionnaire) == questionnaire.title

    def test_question_creation(self):
        questionnaire = baker.make(Questionnaire)
        question = baker.make(Question, questionnaire=questionnaire)
        assert isinstance(question, Question)
        assert str(question) == question.question_text

    def test_question_choice_creation(self):
        question = baker.make(Question)
        choice = baker.make(QuestionChoice, question=question)
        assert isinstance(choice, QuestionChoice)
        assert str(choice) == choice.value

    def test_response_creation(self):
        questionnaire = baker.make(Questionnaire)
        response = baker.make(Response, questionnaire=questionnaire)
        assert isinstance(response, Response)
        assert (
            str(response)
            == f"{response.respondent}'s response to {response.questionnaire}"
        )

    def test_answer_creation(self):
        question = baker.make(Question)
        response = baker.make(Response)
        answer = baker.make(Answer, question=question, response=response)
        assert isinstance(answer, Answer)
        assert str(answer) == f"Answer to {question}"

    def test_answer_choice_creation(self):
        choice = baker.make(QuestionChoice)
        answer = baker.make(Answer)
        answer_choice = baker.make(AnswerChoice, question_choice=choice, answer=answer)
        assert isinstance(answer_choice, AnswerChoice)
        assert str(answer_choice) == str(choice)
