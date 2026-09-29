// Render one page of a PDF (or a PDF-compatible .ai) to a transparent PNG, cropped to its ArtBox.
// For files macOS `sips` can't open (PJOR_Logo.ai, 2026-09-29). No installs: Swift + CoreGraphics ship with macOS.
//
//   swift tools/render_pdf.swift "in.ai" out.png [width_px]
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 3, let doc = CGPDFDocument(URL(fileURLWithPath: a[1]) as CFURL), let page = doc.page(at: 1) else {
    print("usage: swift render_pdf.swift in.pdf out.png [width]"); exit(1)
}
let box = page.getBoxRect(.artBox)
let width = a.count > 3 ? Double(a[3])! : 2400
let s = width / Double(box.width)
let W = Int(width), H = Int((Double(box.height) * s).rounded())
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.clear(CGRect(x: 0, y: 0, width: W, height: H))
ctx.scaleBy(x: CGFloat(s), y: CGFloat(s))
ctx.translateBy(x: -box.minX, y: -box.minY)
ctx.drawPDFPage(page)
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dest)
print("\(a[2]) \(W) x \(H), art box \(box.width / 72) x \(box.height / 72) in")
