#[derive(Debug, Clone, Copy, Default, PartialEq)]
struct Point(i128, i128);

#[derive(Debug, Clone, PartialEq)]
struct Polyline{
    ps:Vec<Point>
}

impl Polyline{
    fn create_polyline(p:Point)->Polyline{
        Polyline{
            ps:vec![p]
        }
    }
    fn add_point(&mut self,p:Point){
        self.ps.push(p);
    }
    fn get_point(&self,i:usize)->Option<Point>{
        if i<self.ps.len(){
            Some(self.ps[i])
        }
        else{
            None
        }
    }

    fn remove_point(&mut self,i:usize)->Result<(),&'static str>{
        if self.ps.len()<=1{
            return Err("can`t be empty");
        }
        if i>=self.ps.len(){
            return Err("Out-of-bounds memory access");
        }
        self.ps.remove(i);
        Ok(())
    }
}

fn main(){
    let p1=Point::create_point(1,2);
    let p2=Point::create_point(2,3);
    let mut line =Polyline::create_polyline(p1);
    let _=line.add_point(p2);
    println!("{:?}", line);
    let _=line.remove_point(0);
    if let Err(e)=line.remove_point(0){
        println!(":{}",e);
    }
}