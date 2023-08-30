package handlers

import (
	"encoding/json"
	"errors"
	// "log"
	// "io/ioutil"
	"net/http"

	"server/helpers"
	"server/models"
	// "server/types"
	// "github.com/go-chi/chi/v5"
)

var user models.User

func GetAllUsers(w http.ResponseWriter, r *http.Request) {
	users, err := user.FindAll()

	if err != nil {
		helpers.MessageLogs.ErrorLog.Println(err)
		helpers.ErrorJSON(w, errors.New("No users found"), http.StatusInternalServerError)
		return
	}

	helpers.WriteJSON(w, http.StatusOK, users)
}

func CreateUser(w http.ResponseWriter, r *http.Request) {
	var userData models.User

	// log.Println("Body: ", r.Body)
	helpers.MessageLogs.InfoLog.Println("Body: ", r.Body)

	err := json.NewDecoder(r.Body).Decode(&userData)
	// body, err := ioutil.ReadAll(r.Body)
	// err = json.Unmarshal(body, &userData)

	helpers.MessageLogs.InfoLog.Println("userData", userData)

	if err != nil {
		helpers.MessageLogs.ErrorLog.Println(err)
		helpers.ErrorJSON(w, errors.New("Invalid JSON"), http.StatusBadRequest)
		return
	}

	// helpers.WriteJSON(w, http.StatusOK, userData)

	// log.Println("userData", userData)
	helpers.MessageLogs.InfoLog.Println("userData", userData)

	if err != nil {
		helpers.MessageLogs.ErrorLog.Println(err)
		helpers.ErrorJSON(w, errors.New("Invalid JSON"), http.StatusBadRequest)
		return
	}

	newUser, err := user.Create(userData)

	if err != nil {
		helpers.MessageLogs.ErrorLog.Println(err)
		helpers.ErrorJSON(w, errors.New("Error creating user"), http.StatusInternalServerError)
		return
	}

	helpers.WriteJSON(w, http.StatusOK, newUser)
}
