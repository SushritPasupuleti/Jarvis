package models

import (
	"context"
	"errors"
	"log"
	"time"

	"github.com/gofrs/uuid"
)

type User struct {
	ID         uuid.UUID `json:"id"`
	name       string    `json:"name"`
	email      string    `json:"email"`
	password   string    `json:"password"`
	created_at time.Time `json:"created_at"`
	updated_at time.Time `json:"updated_at"`
}

func (u *User) Create() error {
	ctx, cancel := context.WithTimeout(context.Background(), dbTimeout)

	defer cancel()

	query := `INSERT INTO users (name, email, password, created_at, updated_at) VALUES ($1, $2, $3, $4, $5) RETURNING *`

	rows, err := db.QueryContext(ctx, query, u.name, u.email, u.password, time.Now(), time.Now())
	if err != nil {
		log.Println(err)
		return err
	}

	var users []*User
	for rows.Next() {
		var user User
		err := rows.Scan(&user.ID, &user.name, &user.email, &user.password, &user.created_at, &user.updated_at)
		if err != nil {
			log.Println(err)
			return err
		}

		users = append(users, &user)
	}

	if len(users) == 0 {
		return errors.New("No user found")
	}

	return nil
}

func (u *User) FindAll() ([]*User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), dbTimeout)

	defer cancel()

	query := `SELECT id, name, email, password, created_at, updated_at FROM users`

	rows, err := db.QueryContext(ctx, query)
	if err != nil {
		log.Println(err)
		return nil, err
	}

	var users []*User
	for rows.Next() {
		var user User
		err := rows.Scan(&user.ID, &user.name, &user.email, &user.password, &user.created_at, &user.updated_at)
		if err != nil {
			log.Println(err)
			return nil, err
		}

		users = append(users, &user)
	}

	if len(users) == 0 {
		return nil, errors.New("No user found")
	}

	return users, nil
}

func (u *User) FindByEmail() error {
	ctx, cancel := context.WithTimeout(context.Background(), dbTimeout)

	defer cancel()

	query := `SELECT id, name, email, password, created_at, updated_at FROM users WHERE email = $1`

	rows, err := db.QueryContext(ctx, query, u.email)
	if err != nil {
		log.Println(err)
		return err
	}

	var users []*User
	for rows.Next() {
		var user User
		err := rows.Scan(&user.ID, &user.name, &user.email, &user.password, &user.created_at, &user.updated_at)
		if err != nil {
			log.Println(err)
			return err
		}

		users = append(users, &user)
	}

	if len(users) == 0 {
		return errors.New("No user found")
	}

	u.ID = users[0].ID
	u.name = users[0].name
	u.email = users[0].email
	u.password = users[0].password
	u.created_at = users[0].created_at
	u.updated_at = users[0].updated_at

	return nil
}

func (u *User) UpdateByEmail() error {
	ctx, cancel := context.WithTimeout(context.Background(), dbTimeout)

	defer cancel()

	query := `UPDATE users SET name = $1, email = $2, password = $3, updated_at = $4 WHERE email = $5`

	_, err := db.ExecContext(ctx, query, u.name, u.email, u.password, time.Now(), u.email)
	if err != nil {
		log.Println(err)
		return err
	}

	return nil
}
