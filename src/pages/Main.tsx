import React, { FC, useEffect,  useState } from 'react'
import PostService from '../API/PostService'
import { useNavigate } from 'react-router-dom'
import 'react-calendar-datetime-picker/dist/style.css'
import IEvent from '../API/models/ins'
import {IDate} from '../types/types'
import Event from '../components/Event'
import FormCalendar from '../components/FormCalendar'

const Main: FC = () =>{

  const [userName, setUserName] = useState<string>('')

  const [date, setDate] = useState<IDate>({'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11})

  const [eventName, setEventName] = useState<string>('')

  const [events, setEvents] = useState<Array<IEvent>>([])

  const navigate = useNavigate()

  useEffect(() => {
    if (localStorage.getItem('token')){
      fetchGetUser(String(localStorage.getItem('token')))
      fetchGetEvents(String(localStorage.getItem('token')))
    }
    else{
      navigate('/login')
    }  
  }, [localStorage])


  async function fetchGetUser (token: string) {
    const response = await PostService.getUser(token)

    if (response.userName) {
      setUserName(response.userName)
    } else {
      navigate('/login')
    }
  }

  async function fetchCreateEvent (token: string, name: string, time:IDate) {
    const response = await PostService.createEvent(token, name, time)

    if (response) {
      fetchGetEvents(String(localStorage.getItem('token')))
    } 
  }

  async function fetchDeleteEvent (token: string, name: string, time:IDate) {
    const response = await PostService.deleteEvent(token, name, time)

    if (response) {
      fetchGetEvents(String(localStorage.getItem('token')))
    } 
  }

  async function fetchGetEvents (token: string) {
    const response = await PostService.getEvents(token)

    if (response) {
      setEvents(response)
    } 
  }

  const onSubmit = (e: React.FormEvent<HTMLFormElement>)=>{
    e.currentTarget.click()
    e.preventDefault()

    fetchCreateEvent(String(localStorage.getItem('token')), eventName, date)
  }

  const onChangeEvent =(e: React.ChangeEvent<HTMLInputElement>)=>{
    setEventName(e.target.value.toLowerCase())
  }

  const onClickHistory = (e: React.MouseEvent<HTMLElement>)=>{
    e.preventDefault()
    navigate('/history')
  }

  return (
    <div>
      <div className='top'>
        <h1>Как часто, {userName}?</h1>
        <a className="linkHistory"onClick={onClickHistory}>ИСТОРИЯ</a>
        </div>
        
        <FormCalendar onSubmit={onSubmit} onChangeEvent={onChangeEvent} setDate={setDate} eventName={eventName} type={false} events={events}/>

        {events &&
          <div>
            {events.map( (event, index) => <Event name={event.name} time={event.time} key={index} fetchDeleteEvent={fetchDeleteEvent}/> )}
            </div>
        }
    </div>
  )
}

export default Main
