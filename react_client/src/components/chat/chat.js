import React, { Component } from 'react'
import ChatInput from './chat.component'
import ChatMessage from '../message/message.component'

const URL = 'ws://localhost:9000'

class Chat extends Component {
	state = {
		name: 'Michal',
		messages: [],
	}

	ws = new WebSocket(URL)

	componentDidMount() {
		this.ws.onopen = (e) => {
		}

		this.ws.onmessage = event => {
			const message = JSON.parse(event.data)
			this.addMessage(message)
		}

		this.ws.onclose = () => {
			console.log("disconnected")
			this.setState({
				ws: new WebSocket(URL),
			})
		}
	}

	addMessage = message =>
		this.setState(state => ({ messages: [message, ...state.messages]
	}))

	submitMessage = messageString => {
		const message = { name: this.state.name, message: messageString }
		this.ws.send(JSON.stringify(message))
	}

	render() {
		return (
		  <div>
	        <label htmlFor="name">
	          Name:&nbsp;
	          <input
	            type="text"
	            id={'name'}
	            placeholder={'Enter your name...'}
	            value={this.state.name}
	            onChange={e => this.setState({ name: e.target.value })}
	          />
	        </label>
	        <ChatInput
	          ws={this.ws}
	          onSubmitMessage={messageString => this.submitMessage(messageString)}
	        />
	        {this.state.messages.map((message, index) =>
	          <ChatMessage
	            key={index}
	            message={message.message}
	            name={message.name}
	          />,
	        )}
	      </div>
		)
	}
}

export default Chat
