import Foundation
import Vision
import CoreImage
import AppKit

// Usa o mesmo motor de recorte de assunto do Preview do macOS.
// Local, sem rede, sem servico externo.
let args = CommandLine.arguments
guard args.count >= 3 else { print("uso: recorta <entrada> <saida.png>"); exit(1) }
let src = URL(fileURLWithPath: args[1])
let dst = URL(fileURLWithPath: args[2])

guard let ciImage = CIImage(contentsOf: src) else { print("nao abriu"); exit(1) }
let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
let req = VNGenerateForegroundInstanceMaskRequest()
do { try handler.perform([req]) } catch { print("falhou: \(error)"); exit(1) }
guard let obs = req.results?.first else { print("sem assunto detectado"); exit(1) }

do {
    let masked = try obs.generateMaskedImage(ofInstances: obs.allInstances,
                                             from: handler, croppedToInstancesExtent: true)
    let ci = CIImage(cvPixelBuffer: masked)
    let ctx = CIContext()
    guard let cg = ctx.createCGImage(ci, from: ci.extent) else { print("sem cgimage"); exit(1) }
    let rep = NSBitmapImageRep(cgImage: cg)
    guard let png = rep.representation(using: .png, properties: [:]) else { print("sem png"); exit(1) }
    try png.write(to: dst)
    print("ok \(Int(ci.extent.width))x\(Int(ci.extent.height))")
} catch { print("erro: \(error)"); exit(1) }
