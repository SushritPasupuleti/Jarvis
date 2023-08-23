package main

// A simple program demonstrating the text area component from the Bubbles
// component library.

import (
	"fmt"
	"log"
	"strings"
	"os/exec"
	"github.com/charmbracelet/bubbles/textarea"
	"github.com/charmbracelet/bubbles/viewport"
	"github.com/charmbracelet/bubbles/spinner"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

func main() {
	p := tea.NewProgram(initialModel())

	if _, err := p.Run(); err != nil {
		log.Fatal(err)
	}
}

func execJarvis(message string) string {
	// commands := []string{"pwd"}
	// commands := []string{"pwd"}
	cmd := exec.Command("./run.sh", message)
	// cmd := exec.Command(strings.Join(commands, " "))
	cmd.Dir = "../model"
	out, err := cmd.Output()
	if err != nil {
		// println("Error: ", err.Error())
		return "Error: " + err.Error()
	}
	// fmt.Println(string(out))

	return string(out)
}

// func execJarvisAsync() <-chan string {
// 	reply := make(chan string)
//
// 	go func() {
// 		defer close(reply)
//
// 		reply <- execJarvis()
// 	}()
//
// 	return reply
// }

type (
	errMsg error
)

type model struct {
	viewport    viewport.Model
	spinner  spinner.Model
	messages    []string
	textarea    textarea.Model
	senderStyle lipgloss.Style
	replyStyle  lipgloss.Style
	err         error
	thinking bool
}

func initialModel() model {
	ta := textarea.New()
	ta.Placeholder = "Send a message..."
	ta.Focus()

	ta.Prompt = "┃ "
	// ta.CharLimit = 280

	ta.SetWidth(300)
	ta.SetHeight(3)

	s := spinner.New()
	s.Spinner = spinner.Dot
	s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
	s.Tick()

	// Remove cursor line styling
	ta.FocusedStyle.CursorLine = lipgloss.NewStyle()

	ta.ShowLineNumbers = false

	// vp := viewport.New(30, 5)
	vp := viewport.New(300, 50)
	vp.SetContent(`Welcome to the chat room!
Type a message and press Enter to send.`)

	ta.KeyMap.InsertNewline.SetEnabled(false)

	return model{
		textarea:    ta,
		messages:    []string{},
		spinner:  s,
		viewport:    vp,
		senderStyle: lipgloss.NewStyle().Foreground(lipgloss.Color("5")),
		replyStyle:  lipgloss.NewStyle().Foreground(lipgloss.Color("3")),
		err:         nil,
	}
}

func (m model) Init() tea.Cmd {
	// m.spinner.Tick()
	return textarea.Blink
	// return m.spinner.Tick
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var (
		tiCmd tea.Cmd
		vpCmd tea.Cmd
	)

	m.textarea, tiCmd = m.textarea.Update(msg)
	m.viewport, vpCmd = m.viewport.Update(msg)

	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.Type {
		case tea.KeyCtrlC, tea.KeyEsc:
			fmt.Println(m.textarea.Value())
			return m, tea.Quit
		case tea.KeyEnter:

			m.thinking = true
			m.messages = append(m.messages, m.senderStyle.Render("You: ")+m.textarea.Value())

			var reply string
			reply = execJarvis(m.textarea.Value())

			m.messages = append(m.messages, m.replyStyle.Render("Jarvis: ") + reply)
			m.thinking = false

			m.viewport.SetContent(strings.Join(m.messages, "\n"))
			m.textarea.Reset()
			m.viewport.GotoBottom()

			return m, nil
		}

	// We handle errors just like any other message
	case errMsg:
		m.err = msg
		return m, nil
	default:
		var cmd tea.Cmd
		m.spinner, cmd = m.spinner.Update(msg)
		return m, cmd
	}

	return m, tea.Batch(tiCmd, vpCmd)
}

func (m model) View() string {

	var spinner string

	if m.thinking == true {
		spinner = m.spinner.View() + "Thinking... \n\n"
	} else {
		spinner = ""
	}

	return fmt.Sprintf(
		"%s\n\n%s",
		m.viewport.View(),
		// m.spinner.View() + "Thinking... \n\n" +
		spinner +
		m.textarea.View(),
	) + "\n\n"
}
