import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


const DUMMY_DATA = [
  {
    senderId: "perborgen",
    text: "who'll win?"
  },
  {
    senderId: "janedoe",
    text: "who'll win?"
  }
]

class App extends React.Component {
  constructor() {
    super()
    this.state = {
       messages: DUMMY_DATA
    }
  }

  render() {
    return (
      <div className="app">
        <Title />
        <MessageList messages={this.state.messages}/>
        {/* <SendMessageForm /> */}
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

ReactDOM.render(<App />, document.getElementById('root'));