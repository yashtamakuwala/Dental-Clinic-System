import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


const DUMMY_DATA = [
  {
    senderId: "Botez",
    text: "Hello"
  },
  {
    senderId: "Yash",
    text: "Hi"
  }
]

class App extends React.Component {
  constructor() {
    super()
    this.state = {
       messages: DUMMY_DATA
    }

    this.sendMessage = this.sendMessage.bind(this)
  }

  sendMessage(text) {
    var msg = {senderId: "ab", text: text}
    DUMMY_DATA.push(msg)
    this.setState({
      messages: DUMMY_DATA
    })
  }

  render() {
    return (
      <div className="app">
        <Title />
        <MessageList messages={this.state.messages}/>
        <SendMessageForm sendMessage={this.sendMessage}/>
     </div>
    )
  }
}

class MessageList extends React.Component {

  render() {
    return (
      <ul className="message-list">                 
        {this.props.messages.map((message, index) => {
          return (
           <li key={index}>
             <div>
               <b>{message.senderId}</b>
             </div>
             <div>
               {message.text}
             </div>
           </li>
         )
       })}
     </ul>
    )
  }
}

function Title() {
  return <p className="title">My Dental Clinic chat bot</p>
}

class SendMessageForm extends React.Component {
  constructor() {
      super()
      this.state = {
          message: ''
      }
      this.handleChange = this.handleChange.bind(this)
      this.handleSubmit = this.handleSubmit.bind(this)
  }
  
  handleChange(e) {
      this.setState({
          message: e.target.value
      })
  }
  
  handleSubmit(e) {
      e.preventDefault()
      this.props.sendMessage(this.state.message)
      this.setState({
          message: ''
      })
  }
  
  render() {
      return (
          <form
              onSubmit={this.handleSubmit}
              className="send-message-form">
              <input
                  onChange={this.handleChange}
                  value={this.state.message}
                  placeholder="Type your message and hit ENTER"
                  type="text" />
          </form>
      )
  }
}


ReactDOM.render(<App />, document.getElementById('root'));