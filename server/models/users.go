package models

import (
	"context"
	"errors"
	"log"
	"time"

	"github.com/gofrs/uuid"
)

type User struct {
	ID         uuid.UUID `json:"id,omitempty"`
	Name       string    `json:"name,omitempty"`
	Emai      string    `json:"email,omitempty"`
	Password   string    `json:"password,omitempty"`
	CreatedAt time.Time `json:"created_at,omitempty"`
	UpdatedAt time.Time `json:"updated_at,omitempty"`
}

func (u *User) Create(user User) (*User, error) {
	ctx, cancel := context.WithTimeout(context.Background(), dbTimeout)

	defer cancel()

	query := `INSERT INTO users (name, email, password, created_at, updated_at) VALUES ($1, $2, $3, $4, $5) RETURNING *`

	_, err := db.ExecContext(
		ctx,
		query,
		user.Name,
		user.Emai,
		user.Password,
		time.Now(),
		time.Now(),
	)	

	if err != nil {	
		log.Println(err)
		return nil, err
	}

	return &user, nil
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
		err := rows.Scan(&user.ID, &user.Name, &user.Emai, &user.Password, &user.CreatedAt, &user.UpdatedAt)
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

	rows, err := db.QueryContext(ctx, query, u.Emai)
	if err != nil {
		log.Println(err)
		return err
	}

	var users []*User
	for rows.Next() {
		var user User
		err := rows.Scan(&user.ID, &user.Name, &user.Emai, &user.Password, &user.CreatedAt, &user.UpdatedAt)
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
	u.Name = users[0].Name
	u.Emai = users[0].Emai
	u.Password = users[0].Password
	u.CreatedAt = users[0].CreatedAt
	u.UpdatedAt = users[0].UpdatedAt

	return nil
}

func (u *User) UpdateByEmail() error {
	ctx, cancel := context.WithTimeout(context.Background(), dbTimeout)

	defer cancel()

	query := `UPDATE users SET name = $1, email = $2, password = $3, updated_at = $4 WHERE email = $5`

	_, err := db.ExecContext(ctx, query, u.Name, u.Emai, u.Password, time.Now(), u.Emai)
	if err != nil {
		log.Println(err)
		return err
	}

	return nil
}
