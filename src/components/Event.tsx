import React, { FC, useEffect, useState } from 'react'
import IEvent from '../API/models/ins'
import Time from '../components/Time'
import { DtPicker} from 'react-calendar-datetime-picker'
import 'react-calendar-datetime-picker/dist/style.css'
import {IDate} from '../types/types'
import {IRangeDate} from '../types/types'

interface IEventProps extends IEvent{
    fetchDeleteEvent: (token: string, name: string, time: IDate)=>void
}

const Event:FC<IEventProps> = ({name, time, fetchDeleteEvent}:IEventProps) =>{
    return(
        <div>
            <div>{name}
            
           </div>
            {time.map( (tim)=><Time date={tim} fetchDeleteEvent={fetchDeleteEvent} name={name}/>)}
        </div>
    )
}

export default Event

