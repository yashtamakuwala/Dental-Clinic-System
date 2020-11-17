import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


const DUMMY_DATA = [
  {
    senderId: "Dental Bot",
    text: "Hello, what is your name?",
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

  sendMessage(text, senderId) {
    var msg = {senderId: senderId, text: text}
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
             {
              ( message.senderId  === "Dental Bot") ? 
              <div>
                {message.text}
              </div> : 
                 <div>
                 <b>{message.text} </b>
                 </div> 
             }
            
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
          message: '',
          isLoaded : false,
          error: null,
          items: [],
          patient : ''
      }
      this.handleChange = this.handleChange.bind(this)
      this.handleSubmit = this.handleSubmit.bind(this)


  }
  
  handleChange(e) {
      this.setState({
          message: e.target.value
      })
      
  }
  
  
  async handleSubmit(e) {
      e.preventDefault()
      this.props.sendMessage(this.state.message, this.state.patient)
      this.setState({
          message: ''
      })

      await fetch("http://localhost:5000/v1/ask?message="+this.state.message + '&patient='+this.state.patient)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        items: result,
                        patient : result.name
                    });
                    console.log(result)
                    

                },
                // Note: it's important to handle errors here
                // instead of a catch() block so that we don't swallow
                // exceptions from actual bugs in components.
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )
            this.props.sendMessage(this.state.items.answer, "Dental Bot")
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