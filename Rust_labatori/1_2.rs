use std::fmt::Debug;
use std::pin::Pin;
use std::rc::Rc;

pub trait SayHi:Debug{
    fn say_hi(self:Pin<&Self>){
        println!("{:?}",self);
    }
}

pub trait MutMeSomehow{
    fn mut_me_somehow(self:Pin<&mut Self>);
}

mod impls{
    use super::*;
    impl SayHi for String{}
    impl MutMeSomehow for String{
        fn mut_me_somehow(self:Pin<&mut Self>){
            self.get_mut().push_str("!");
        }
    }
    impl<T:Debug>SayHi for Vec<T>{}
    impl<T>MutMeSomehow for Vec<T>{
        fn mut_me_somehow(mut self:Pin<&mut Self>){
            self.set(vec![]);
        }
    }
    impl<T:Debug> SayHi for Box<T>{}
    impl<T:Default> MutMeSomehow for Box<T>{
        fn mut_me_somehow(self:Pin<&mut Self>){
            **self.get_mut()=T::default();
        }
    }
    impl SayHi for &[u8]{}
    impl MutMeSomehow for &[u8]{
        fn mut_me_somehow(self:Pin<&mut Self>){
            let slice=self.get_mut();
            if !slice.is_empty(){
                *slice=&slice[1..];
            }
        }
    }
    impl<T:Debug> SayHi for Rc<T>{}
    impl<T:Default> MutMeSomehow for Rc<T>{
        fn mut_me_somehow(self:Pin<&mut Self>){
            if let Some(val)=Rc::get_mut(self.get_mut()){
                *val=T::default();
            }
        }
    }
    #[derive(Debug,Default)]
    pub struct Node(pub i32);
    impl SayHi for Node{}
    impl MutMeSomehow for Node{
        fn mut_me_somehow(mut self:Pin<&mut Self>){
            self.as_mut().get_mut().0 += 1;
        }
    }
}
fn main(){
    use impls::*;
    let mut s=String::from("Rustbootcamp");
    Pin::new(&s).say_hi();
    Pin::new(&mut s).mut_me_somehow();
    println!("Str:{}\n",s);

    let mut v=vec![1,2,3];
    Pin::new(&v).say_hi();
    Pin::new(&mut v).mut_me_somehow();
    println!("Vec:{:?}\n",v);

    let mut b=Box::new(42);
    Pin::new(&b).say_hi();
    Pin::new(&mut b).mut_me_somehow();
    println!("Box:{:?}\n",b);

    let bytes:&[u8]=&[10,20,30];
    let mut slice_ref=bytes;
    Pin::new(&slice_ref).say_hi();
    Pin::new(&mut slice_ref).mut_me_somehow();
    println!("Slice:{:?}\n",slice_ref);

    let mut rc=Rc::new(100);
    Pin::new(&rc).say_hi();
    Pin::new(&mut rc).mut_me_somehow();
    println!("Rc:{:?}\n",rc);

    let mut node=Node(5);
    Pin::new(&node).say_hi();
    Pin::new(&mut node).mut_me_somehow();
    println!("Node:{:?}\n",node);
}