package models

import (
	"context"
	"errors"
	"time"

	"github.com/gofrs/uuid"
)

type Question struct {
	ID         uuid.UUID `json:"id"`
	question   string    `json:"question"`
	answer     string    `json:"answer"`
	created_at time.Time `json:"created_at"`
	updated_at time.Time `json:"updated_at"`
	user_id    uuid.UUID `json:"user_id"`
}

func (q *Question) Create() error {
	ctx, cancel := context.WithTimeout(context.Background(), dbTimeout)

	defer cancel()

	query := `INSERT INTO questions (question, answer, created_at, updated_at, user_id) VALUES ($1, $2, $3, $4, $5) RETURNING *`

	rows, err := db.QueryContext(ctx, query, q.question, q.answer, time.Now(), time.Now(), q.user_id)
	if err != nil {
		return err
	}

	var questions []*Question
	for rows.Next() {
		var question Question
		err := rows.Scan(&question.ID, &question.question, &question.answer, &question.created_at, &question.updated_at, &question.user_id)
		if err != nil {
			return err
		}

		questions = append(questions, &question)
	}

	if len(questions) == 0 {
		return errors.New("No question found")
	}

	return nil
}

func (q *Question) FindAll() ([]*Question, error) {
	ctx, cancel := context.WithTimeout(context.Background(), dbTimeout)

	defer cancel()

	query := `SELECT id, question, answer, created_at, updated_at, user_id FROM questions`

	rows, err := db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}

	var questions []*Question
	for rows.Next() {
		var question Question
		err := rows.Scan(&question.ID, &question.question, &question.answer, &question.created_at, &question.updated_at, &question.user_id)
		if err != nil {
			return nil, err
		}

		questions = append(questions, &question)
	}

	if len(questions) == 0 {
		return nil, errors.New("No question found")
	}

	return questions, nil
}
