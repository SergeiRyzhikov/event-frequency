import React, { FC, useEffect, useState } from 'react'
import PostService from '../API/PostService'
import { useNavigate } from 'react-router-dom'
import IEvent from '../API/models/ins'
import {IDate} from '../types/types'
import {IRangeDate} from '../types/types'
import FormCalendar from '../components/FormCalendar'

const History:FC = ()=> {

    
    const navigate = useNavigate()

    const [userName, setUserName] = useState<string>('')

    const [events, setEvents] = useState<IEvent[]>([])

    const [eventName, setEventName] = useState<string>('')

    const [date, setDate] = useState<IDate>({'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11})

    const [rangeDate, setRangeDate] = useState<IRangeDate>({'from': {'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11}, 'to': {'year':2023, 'month':12, 'day':20, 'hour':23, 'minute':11}})

    const [currentDates, setCurrentDates] = useState<IDate[]>([])
    
    const isInclude = (from: IDate, to:IDate, time: IDate) =>{
      let key: keyof IDate
      let flag1: boolean = true
      let flag2: boolean = true
      
      for (key in time){
        if (from[key] < time[key] ){
          flag1 = true
          break
        }
        if (from[key] > time[key]) {
          flag1 = false
          break
        }
      }
      for (key in time){
        if (to[key] > time[key] ){
          flag2 = true
          break
        }
        if (to[key] < time[key]) {
          flag2 = false
          break
        }
      }
      if (flag1 && flag2){
        return true
      }
      else{
        return false
      }
    }
    async function fetchGetUser (token: string) {
        console.log('jjjj')
        const response = await PostService.getUser(token)
        console.log('kk')
        if (response.userName) {
          setUserName(response.userName)
          console.log(response.userName)
        } else {
          navigate('/login')
          console.log('34')
        }
      }

    async function fetchGetEvents (token: string) {
        const response = await PostService.getEvents(token)
        console.log(response)
        if (response) {
          setEvents(response)
          if (response[0]){
            setEventName(response[0].name)
          }
          console.log(response)
        } else {
          console.log('34')
        }
      }

    const onSubmit = (e: React.FormEvent<HTMLFormElement>)=>{
      e.currentTarget.click()
      e.preventDefault()
      let currentEventDates: Array<IDate> = []
      // сделал запрос
      setCurrentDates([])
      for (let i=0; i < events.length; i++){
        if(events[i].name==eventName){
          let eventDates = events[i].time
          // const currentEventDates = []
          currentEventDates = eventDates.filter((checkDate)=> isInclude(rangeDate.from, rangeDate.to, checkDate))
          break
      }}
      if (currentEventDates.length !==0){
        currentEventDates.sort((a, b)=> {
          let key: keyof IDate
          let flag = 0
          for (key in a){
            if (a[key] < b[key] ){
              flag = -1
              break
            }
            if (a[key] > b[key]) {
              flag = 0
              break
            }
          }
          return flag
        })
        setCurrentDates(currentEventDates)
      }
    }
    const onClickMain = (e: React.MouseEvent<HTMLElement>)=>{
      e.preventDefault()
      navigate('/')
    }
    
    useEffect(() => {
        console.log('useEffect')
        if (localStorage.getItem('token')){
          fetchGetUser(String(localStorage.getItem('token')))
          fetchGetEvents(String(localStorage.getItem('token')))
        }
        else{
          navigate('/login')
        }
        console.log(isInclude({'year':2025, 'month':12, 'day':20, 'hour':23, 'minute':11}, {'year':2025, 'month':12, 'day':20, 'hour':23, 'minute':11}, {'year':2025, 'month':12, 'day':20, 'hour':23, 'minute':11},))
    }, [localStorage])

    
    return(
        <div>
          <div className='topHistory'>
          <h1 className="headerHistory">История</h1>
          <a className="linkMain"onClick={onClickMain}>Главная</a>
          </div>
          <FormCalendar onSubmit={onSubmit}  onChangeEvent={setEventName} setDate={setRangeDate} eventName={eventName} type={true} events={events}/>
          {currentDates.length !== 0 ?
            <div>
            <div>Событие - <strong>{eventName}</strong> ||||||||||||| количество - <strong>{currentDates.length}</strong> </div>
            <div>
            {currentDates.map( (date)=> <div>{date.year}.{date.month}.{date.day}  {date.hour}:{date.minute}</div>)}
            </div>
            </div>
            :
            <div>за указанный период события - <strong>{eventName}</strong> - вы не делали</div>
          }
        </div>
    )
}
export default History