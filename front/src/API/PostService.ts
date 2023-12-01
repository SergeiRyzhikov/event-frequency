import axios, { AxiosResponse } from "axios"
import { type } from "os"
import IEvent from "./models/ins"

import Idate from '../types/types'
export default class PostService {
    baseUrl = 'http://127.0.0.1:8000'

    static async login(userName:string, password:string){
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/users',
        { 'userName': userName, 'password': password },
        {headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          }})
        return response.data
        } catch(e){
            console.log(typeof(e))
        }   
    }
    static async verify(userName:string, password:string){
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/users/token',
        { 'userName': userName, 'password': password },
        {headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          }})
        return response.data
        } catch(e){
            console.log(e)
        }   
    }
    static async getUser(token:string){
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/users/me',
        { 'token': token },
        {headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          }})
        return response.data
        } catch(e){
            console.log(e)
        }   
    }

    static async createEvent(token:string, name: string, time: Idate){
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/create_event',
            {
                "event": {
                  'name': name,
                  'time': time
                },
                "token": {
                  "token": token
                }
              },
        {headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          }})
        return response.data
        } catch(e){
            console.log(e)
        }   
    }

    static async getEvents(token:string){
        try {
            const response = await axios.post<Array<IEvent>>('http://127.0.0.1:8000/api/events/me',
            {'token': token
            },
        {headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          }})
        return response.data
        } catch(e){
            console.log(e)
        }   
    }
    static async deleteEvent(token:string, name: string, time: Idate){
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/delete_event',
            {
                "event": {
                  'name': name,
                  'time': time
                },
                "token": {
                  "token": token
                }
              },
        {headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          }})
        return response.data
        } catch(e){
            console.log(e)
        }   
    }
}